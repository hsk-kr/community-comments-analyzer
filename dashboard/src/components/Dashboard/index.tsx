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
      count: Math.floor(Math.random() * 3000) + 100,
      date: cDate,
    };

    data.push(countOfComments);
  }

  return data;
};

const Dashboard: FunctionComponent<{}> = () => {
  const commentsCountSvgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    // TODO: create a sample bar chart for displaying numbers of comments.
    const svg: any = d3.select(commentsCountSvgRef.current);
    const data: Array<CountOfComments> = createFakeData();

    console.log(data);

    if (!commentsCountSvgRef.current) {
      return;
    }
    // svg size
    const width: number = commentsCountSvgRef.current.offsetWidth; //svg.style('width');
    const height: number = commentsCountSvgRef.current.offsetHeight; //svg.style('height');

    console.log(`width:${width}`);
    console.log(`height:${height}`);

    // yAxis
    const yScale: any = d3
      .scaleLinear()
      .domain(d3.extent<CountOfComments, number>(data, d => d.count) as any)
      .rangeRound([height, 0]);

    const yAxis: any = d3.axisLeft(yScale).ticks(6);

    svg
      .append('g')
      .attr('transform', `translate(50, 50)`)
      .call(yAxis);

    // xAxis
    const xScale: any = d3
      .scaleTime()
      .domain(d3.extent<CountOfComments, Date>(data, d => d.date) as any)
      .rangeRound([0, width]);

    const xAxis: any = d3.axisBottom(xScale).ticks(5);

    svg
      .append('g')
      .attr('transform', `translate(50, ${height + 50})`)
      .call(xAxis);

    // draw line
    const line: any = d3
      .line<CountOfComments>()
      .x(d => xScale(d.date))
      .y(d => yScale(d.count));

    const lineGroup: any = svg
      .append('g')
      .attr('transform', `translate(51, 50)`);

    const lines: any = lineGroup
      .datum(data)
      .append('path')
      .attr('class', 'line')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', '0.1rem')
      .attr('fill', 'none')
      .attr('d', line);

    const totalLength: number = lines.node().getTotalLength();

    lines
      .attr('stroke-dasharray', totalLength)
      .attr('stroke-dashoffset', totalLength)
      .transition()
      .ease(d3.easeLinear)
      .delay(1000)
      .duration(2000)
      .attr('stroke-dashoffset', 0);

    // line mouse event
    const focus: any = svg
      .append('g')
      .attr('class', 'focus')
      .attr('display', 'none');

    focus
      .append('rect')
      .attr('stroke-width', '0.1rem')
      .attr('stroke', 'black')
      .attr('fill', 'none')
      .attr('class', 'tooltip')
      .attr('width', 100)
      .attr('height', 50);

    focus
      .append('text')
      .attr('x', 8)
      .attr('y', 18)
      .attr('class', 'count')
      .style('font-size', '0.8rem')
      .text('count:');

    focus
      .append('text')
      .attr('x', 8)
      .attr('y', 40)
      .attr('class', 'date')
      .style('font-size', '0.8rem')
      .text('date:');

    const dateFormatter = d3.timeFormat('%y-%m-%d');

    function handleMouseMove(this: any, d: any, i: any) {
      const v: any = xScale.invert(d3.mouse(this)[0] - 26);

      const bisectDate: any = d3.bisector((d: CountOfComments) => d.date).left;
      let v2 = bisectDate(data, v) - 1;

      if (v2 === undefined) {
        return;
      }

      v2 = v2 - 1;

      if (data[v2] === undefined) {
        return;
      }

      focus.attr(
        'transform',
        `translate(${xScale(data[v2].date)}, ${yScale(data[v2].count)})`,
      );

      focus.select('.count').text(`count: ${data[v2].count}`);
      focus.select('.date').text(`date: ${dateFormatter(data[v2].date)}`);
      //xScale.invert(d3.mouse(this)[0]);
      //focus.attr('transform', `translate(${xScale})`);
    }

    svg
      .on('mouseover', () => focus.style('display', 'block'))
      .on('mouseout', () => focus.style('display', 'none'))
      .on('mousemove', handleMouseMove);
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
          <svg className="canvas" ref={commentsCountSvgRef}></svg>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
