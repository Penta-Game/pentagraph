/* eslint-disable no-undef */
const typeOf = (obj) => {
  return {}.toString
    .call(obj)
    .match(/\s(\w+)/)[1]
    .toLowerCase();
};

function checkTypes(args, types) {
  args = [].slice.call(args);
  for (var i = 0; i < types.length; ++i) {
    if (typeOf(args[i]) != types[i]) {
      throw new TypeError("param " + i + " must be of type " + types[i]);
    }
  }
}

let getJSONP = (obj) => {
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest();
    xhr.open(obj.method || "GET", obj.url);
    if (obj.headers) {
      Object.keys(obj.headers).forEach((key) => {
        xhr.setRequestHeader(key, obj.headers[key]);
      });
    }
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.response));
      } else {
        reject(xhr.statusText);
      }
    };
    xhr.onerror = () => reject(xhr.statusText);
    xhr.send(obj.body);
  });
};

function download(filename, text) {
  var element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:text/plain;charset=utf-8," + encodeURIComponent(text)
  );
  element.setAttribute("download", filename);

  element.style.display = "none";
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

const destructureID = (id) => {
  if (typeOf(id) === "number") {
    return id;
  }
  id = id.split("-");
  const type = id[0];
  if (["corner", "junction", "c", "j"].include(type)) {
    return {
      type: type,
      id: id[1],
    };
  } else if (type === "stop" || type === "s") {
    return {
      type: stop,
      start: id[1],
      counter: id[2],
      end: id[3],
    };
  }
};

class Base {
  constructor(data) {
    /*
        Object representing a figure/ Field on the board
        */
    for ([key, val] in Object.entries(data)) {
      this[key] = val;
    }
  }

  calcPos(args) {
    /*
        function for calculating pos based on data given by constructor
        Must return an array with two numbers (int/ float)
        */
    const points = args; //
    return points;
  }

  getAdjacent() {
    /*
        function for getting adjacent Figures/ Fields
        Must return an array with their respective objects
        */
    return this.adjacent;
  }
}

class Figure extends Base {
  /*
    Class representing a Figure (Gray and black stoppers, Players) on the baord
    */

  constructor(data) {
    super(data);
    this.state.position = state;
    this.id = data.id;
    this.color = data.color;
    this.board = data.board;
  }

  setState(state) {
    this.state = state;
  }

  move(data) {
    console.log(data);
    return true;
  }
}

class Stop extends Base {
  constructor(data) {
    super(data);
    this.id = destructureID(data.id);
    this.points = data.points;
  }

  isEmpty(args) {
    for (const _val in Object.values(args.board.figures)) {
      for (const figure in _val) {
        if (figure.position.id === this.id) {
          if (args.return === true) {
            return figure;
          } else {
            return false;
          }
        }
      }
    }
    return true;
  }

  getAdjacent() {
    if (
      (this.id.start >= 6 && this.id.end < 6) ||
      (this.id.start < 6 && this.id.end >= 6)
    ) {
      return [];
    } else if (this.counter === 1 || this.id.counter === 3) {
      return [];
    } else {
      return [];
    }
  }
}

class Point {
  /*
     class representing a point in the coordinate system
     May contain explicit data (id, points) or inexplicit additional data (state)
    */
  constructor(data) {
    this.id = destructureID(data.id);
    this.additional = {};
    for (const key of Object.keys(data)) {
      this.additional[key] = data[key];
    }
    this.angle = data.angle;
    this.points = { x: data.x, y: data.y };
  }
}

class Field extends Point {
  /*
    Corner or junction field (not a stopper)
    */

  constructor(data) {
    super(data);
  }

  getAdjacent(board) {
    return {
      corners: [board.corners[this.id - 1], board.corners[this.id + 1]],
      junctions: [board.junctions[this.id - 6], board.junctions[this.id - 5]],
    };
  }
}

export { Point, Figure, Stop, Field, getJSONP, download };
