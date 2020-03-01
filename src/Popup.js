import React from "react";
//This is the module we used to create the react-popup
import Popup from "reactjs-popup";
//This is the module we used to create the Linechart.
import {
  LineChart,
  ResponsiveContainer,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Label
} from "recharts";

class ControlledPopup extends React.Component {
  constructor() {
    super();
  }

  render() {
    return (<div>
      {/* //This is the header, which includes the country name and flag */}
      <div>
        {this.props.country + " "}
        <img src={require('./png/' + this.props.abrev + '.png')} width="20" height="10"/>
      </div>
      <div className="modal">
        <a className="close" onClick={this.closeModal}>
          &times;
        </a>
        {/* //This is the Linechart, in data={}, this is where we put in the array */}
        <ResponsiveContainer width={550} height={350}>
        <LineChart data={this.props.dat} margin={{
            top: 5,
            right: 5,
            left: 5,
            bottom: 5
          }}>
            //This is adjusting the axis on the graph.
          <XAxis stroke="#000000" dataKey="years"/>
          <YAxis stroke="#000000"/>
          <CartesianGrid stroke="#000000" strokeDasharray="3 3"/>
          <Tooltip/>
          <Legend/>
          <Line type="monotone" dataKey="caseCount" strokeWidth={this.props.reg_fl ? 0:2} stroke= {this.props.reg_fl ? "#8884d8":"#8884d8"} dot={{fill: this.props.reg_fl ? '#8884d8':'#8884d8'}} activeDot={{
                fill: this.props.reg_fl ? "#8884d8":"#8884d8",
                r: 6
              }}/>
          <Line type="monotone" dataKey="logNum" strokeWidth={3} stroke="#82ca9d" dot={false}/>
        </LineChart>
        </ResponsiveContainer>
      </div>
      <div>
        {/* //This includes the blurb for a person twist */}
        {this.props.blurb}
      </div>
    </div>);
  }
}
export default ControlledPopup;
