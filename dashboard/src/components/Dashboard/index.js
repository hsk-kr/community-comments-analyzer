import Dashboard from "./Dashboard";
import { connect } from "react-redux";
import { fetchComments } from "../../redux/comments";

const mapStateToProps = state => ({
  comments: state.comments
});

const mapDispatchToProps = dispatch => ({
  fetchComments: (srtDate, endDate) => dispatch(fetchComments(srtDate, endDate))
});

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard);
