using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;

namespace Anomaly_Detection_Hub.SignalR
{
   public class SignalRHub : Hub
   {
      static string analyserId = "";
      static string databaseId = "";
      public void AnalyserConnect()
      {
         analyserId = Context.ConnectionId;
         Console.WriteLine("Analyser connected with id: " + analyserId);
      }

      public void DatabaseConnect()
      {
         databaseId = Context.ConnectionId;
         Console.WriteLine("Database connected with id: " + databaseId);
      }

      public async Task SendMessage(string groupName, string messageTag, string message)
      {
         switch (messageTag)
         {
            /*Input*/
            case "Input:NewReading": //New reading recieved from input to be sent to analyser.
               {
                  await Clients.Group(analyserId).SendAsync("AnalyseReading", Context.ConnectionId, message);
                  break;
               }
            /*Analyser*/
            case "Analyser:NewPrediction": //New Prediction recieved from analyser to be sent to database
               {
                  await Clients.Group(databaseId).SendAsync("StoreReading", message);
                  break;
               }
            /*Database*/
            case "Database:ProbeInformation"://ProbeInformation recieved from database to be sent to the frontpage of one or more clients
               {
                  await Clients.Group(groupName).SendAsync("UpdateProbeTable", message);
                  break;
               }
            case "Database:ProbeAnomalies"://ProbeAnomalies recieved from database to be sent to the probepage of one or more clients
               {
                  await Clients.Group(groupName).SendAsync("UpdateAnomalyTable", message);
                  break;
               }
            /*FrontPage*/
            case "Frontpage:GetProbeInformation": //Request for probe information made by the frontpage of a client
               {
                  await Clients.Group(databaseId).SendAsync("RetrieveProbeInformation", Context.ConnectionId);
                  break;
               }
            /*ProbePage*/
            case "Probepage:GetProbeAnomalies": //Request for probe anomalies made by the probepage of a client
               {
                  await Clients.Group(databaseId).SendAsync("RetrieveProbeAnomalies", Context.ConnectionId, message);
                  break;
               }
            default: //Default case for when the messagetag is unsupported
               {
                  await Clients.Group(Context.ConnectionId).SendAsync("error", "unsupported messageTag");
                  break;
               }
         }
      }

      public async void addProbe(string serial, string location, string lat, string lon)
      {
         Console.WriteLine("New probe with serialNumber: " + serial);
         try
         {
            await Clients.Group(databaseId).SendAsync("StoreProbeInformation", serial, location, lat, lon);
            await Clients.Group(analyserId).SendAsync("addProbe", serial);
         }
         catch(Exception e)
         {
            Console.WriteLine(e.Message);
         }
      }

      public async void AddClient(string groupName)
      {
         await Groups.AddToGroupAsync(Context.ConnectionId, groupName);
         Console.WriteLine($"Added {Context.ConnectionId} to group: {groupName}");
      }

      public async void RemoveClient(string connectionId)
      {
         await Groups.RemoveFromGroupAsync(Context.ConnectionId, connectionId);
         await Clients.Group(analyserId).SendAsync("removeProbe", connectionId);
         Console.WriteLine($"Cient removed {connectionId}");

      }

      public override Task OnConnectedAsync()
      {
         Console.WriteLine($"Client {Context.ConnectionId} joined the HUB");
         AddClient(Context.ConnectionId);
         return base.OnConnectedAsync();
      }

      public override Task OnDisconnectedAsync(Exception exception)
      {
         Console.WriteLine($"Client {Context.ConnectionId} left the HUB");
         RemoveClient(Context.ConnectionId);
         return base.OnDisconnectedAsync(exception);
      }
   }
}
