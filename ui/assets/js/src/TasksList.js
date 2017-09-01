import React from "react";
import SolutionStatus from "./SolutionStatus";
import Modal from "./Modal";

const ListItem = props => {
  const modalID = `submit_${props.task.id}`;
  return (
    <div>
      <div className="list-group-item">
        <div className="row">
          <div className="col-md-6">
            {props.task.name}
          </div>
          <div className="col-md-1">
            <SolutionStatus task={props.task} />
          </div>
          <div className="col-md-5">
            <div className="btn-group pull-right">
              <a>
                <button className="btn btn-default uppercase" type="button">
                  Solutions
                </button>
              </a>
              <a
                href={`#${modalID}`}
                data-toggle="modal"
                className="btn btn-default uppercase"
              >
                Submit
              </a>
            </div>
          </div>
        </div>
      </div>
      <Modal modalID={modalID} task={props.task} />
    </div>
  );
};

class TasksList extends React.Component {
  render() {
    const { tasks } = this.props;
    return (
      <div className="list-group">
        {tasks.map(task => {
          return <ListItem key={task.id} task={task} />;
        })}
      </div>
    );
  }
}

export default TasksList;
