import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import commentsReducer from "./comments";

export default createStore(
  combineReducers({ comments: commentsReducer }),
  applyMiddleware(thunk)
);
