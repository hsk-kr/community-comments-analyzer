import React, { useRef, useEffect, FunctionComponent } from 'react';
import './styles.scss';
import * as d3 from 'd3';
import { Paper, TextField, Button, Divider } from '@material-ui/core';
import Navbar from '../Navbar';

interface CountOfComments {
  count: number;
  date: Date;
}

// create fake data list of CountOfComments.
const createFakeData = (): Array<CountOfComments> => {
  const data: Array<CountOfComments> = [];

  for (let i = 30; i >= 0; i--) {
    const cDate = new Date();
    cDate.setDate(cDate.getDate() - i);

    const countOfComments: CountOfComments = {
      count: Math.floor(Math.random() * 1000) + 100,
      date: cDate,
    };

    data.push(countOfComments);
  }

  return data;
};

const Dashboard: FunctionComponent<{}> = () => {
  const commentsCountSvgRef = useRef();

  useEffect(() => {
    // TODO: create a sample bar chart for displaying numbers of comments.
    const svg: any = commentsCountSvgRef.current;
    const data = createFakeData();

    // svg setting
    svg
      .append('path')
      .data(data)
      .attr('fill', 'none')
      .attr('stroke', 'red');

    // get size of the svg
    const width: number = svg.attr('width');
    const height: number = svg.attr('height');

    // xAxis
    const x: any = d3.scaleTime().rangeRound([0, width]);
    const xAxis: any = d3.axisBottom(x);

    // yAxis
    const y: any = d3.scaleLinear().rangeRound([height, 0]);
    const yAxis: any = d3.axisBottom(y);

    const xFormat: string = '%Y-%m-%d';
    const parseTime: any = d3.timeParse('%Y-%m-%d');

    x.domain(d3.extent(data, d => parseTime(d.date)));
    y.domain([0, ])
  }, []);

  return (
    <>
      <Navbar />
      <div className="dashboard-container">
        <div className="toolbar">
          <div>
            <TextField
              disabled
              style={{ marginRight: 5 }}
              label="Starting Date"
              defaultValue="Starting Date"
              variant="outlined"
            />
            <TextField
              disabled
              label="Ending Date"
              defaultValue="Ending Date"
              variant="outlined"
            />
          </div>
          <div style={{ marginTop: 5, marginBottom: 20 }}>
            <Button variant="contained" color="primary">
              Select Dates
            </Button>
          </div>
        </div>
        <Divider />
        <div className="count-graph-container">
          <svg ref="commentsCountSvgRef"></svg>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
