import React, { useEffect } from "react";
import { AppBar, Toolbar, Typography } from "@material-ui/core";

const Dashboard = ({ comments, fetchComments }) => {
  useEffect(() => {
    const endDate = new Date();
    const srtDate = new Date();
    srtDate.setDate(new Date().getDate() - 1);
    fetchComments(srtDate, endDate);
  }, [fetchComments]);

  useEffect(() => {
    console.log("comments");
    console.log(comments);
  }, [comments]);

  return (
    <AppBar>
      <Toolbar>
        <Typography variant="h6">CCA Dashboard</Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Dashboard;
