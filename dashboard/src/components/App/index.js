import React from "react";
import "./styles.css";
import { Provider } from "react-redux";
import store from "../../redux";
import Dashboard from "../Dashboard";

function App() {
  return (
    <Provider store={store}>
      <div className="App">
        <Dashboard />
      </div>
    </Provider>
  );
}

export default App;
