import { ES_TYPE_URL } from "../es";
import axios from "axios";

const COMMENTS_FETCH_REQUEST = "COMMENTS_FETCH_REQUEST";
const COMMENTS_FETCH_SUCCESS = "COMMENTS_FETCH_SUCCESS";
const COMMENTS_FETCH_FAILURE = "COMMENTS_FETCH_FAILURE";

const fetchCommentsRequest = () => ({
  type: COMMENTS_FETCH_REQUEST
});

const fetchCommentsSuccess = comments => ({
  type: COMMENTS_FETCH_SUCCESS,
  payload: comments
});

const fetchCommentsFailure = error => ({
  type: COMMENTS_FETCH_FAILURE,
  payload: error
});

export const fetchComments = (srtDate, endDate) => {
  return async dispatch => {
    dispatch(fetchCommentsRequest());

    try {
      const searchUrl = `${ES_TYPE_URL}/_search`;

      const result = await axios.get(searchUrl, {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "true"
        },
        data: {
          query: {
            nested: {
              path: "comments",
              query: {
                range: {
                  "comments.date": {
                    lte: endDate,
                    gte: srtDate
                  }
                }
              }
            }
          }
        }
      });

      fetchCommentsSuccess(result);
    } catch (err) {
      dispatch(fetchCommentsFailure(err));
    }
  };
};

const reducer = (
  state = {
    loading: false,
    comments: {},
    error: ""
  },
  action
) => {
  switch (action.type) {
    case COMMENTS_FETCH_REQUEST:
      return {
        loading: true
      };
    case COMMENTS_FETCH_SUCCESS:
      return {
        loading: false,
        comments: action.payload
      };
    case COMMENTS_FETCH_FAILURE:
      return {
        loading: false,
        error: action.payload
      };
    default:
      return state;
  }
};

export default reducer;
