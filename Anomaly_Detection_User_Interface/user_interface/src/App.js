import './App.css';
import ProbePage from './Pages/ProbePage';
import Frontpage from './Pages/Frontpage';
import NoPage from './Pages/NoPage';
import Layout from './Pages/Layout';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Frontpage />}/>
            <Route path="ProbePage" element={<ProbePage />}/>
            <Route path="*" element={<NoPage />}/>
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;

