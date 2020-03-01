import React from "react";
//This is the module we used to create the react-popup
import Popup from "reactjs-popup";
//This is the module we used to create the Linechart.
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Label
} from "recharts";

class ControlledPopup1 extends React.Component {
  constructor(props) {
    super(props);
    this.submit = this.props.submit.bind(this);
  }
  // <form>
    //    <p> Enter your Date: </p>
    //    <input
    //      type='text'
    //      onChange={this.myDateHandler}
    //    />
    //    </form>

  render() {
    return (<div>
      <form>
  <label>
    Date:
    <input type="text" onChange={this.props.myDateHandler} />
  </label>
  <input type="submit" value="Submit" onClick={this.submit} />
</form>
    </div>);
  }
}
export default ControlledPopup1;
