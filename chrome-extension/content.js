// content.js



function disableKeyScroll() {
  window.addEventListener("keydown", function(e) {
      // space and arrow keys
      if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
          e.preventDefault();
      }
  }, false);
}

// removes snake game from screen
function removeElement(elementId) {
    // Removes an element from the document
    if (document.querySelector('#snakecanvasID')){
      var element = document.getElementById(elementId);
      element.parentNode.removeChild(element);
    }
}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    // if game is already created do nothing
    if (document.querySelector('#snakecanvasID')) return
    // otherwise
    disableKeyScroll()
    var canv = document.createElement("canvas");
    canv.setAttribute("id", "snakecanvasID");
    document.body.appendChild(canv);
    location.href = "#";
    location.href = "#snakecanvasID";
    var canvas = document.querySelector("#snakecanvasID");
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight - 4;

    var x1 = 10;
    var y1 = 10;
    var x2 = (15 * Math.floor(canvas.width / 15)) - 10;
    var y2 = (15 * Math.floor(canvas.height / 15)) - 10;

    // lets draw 2d elements
    var c = canvas.getContext('2d');
    var moveQueue = [];
    var spaceBarPressed = false
    window.addEventListener('keydown', function(event) {
      if (moveQueue.length > 0 &&
        ((event.which == 38 && moveQueue[moveQueue.length - 1] != 40) ||
          (event.which == 40 && moveQueue[moveQueue.length - 1] != 38) ||
          (event.which == 37 && moveQueue[moveQueue.length - 1] != 39) ||
          (event.which == 39 && moveQueue[moveQueue.length - 1] != 37))) {
        moveQueue.push(event.which);
      } else if (moveQueue.length == 0 && event.which <= 40 && event.which >= 38) {
        moveQueue.push(event.which);
      } else if (event.which == 32){
        spaceBarPressed = true
        removeElement("snakecanvasID")
      }
    });

    window.addEventListener('resize', function(event) {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight - 4;
      x2 = (15 * Math.floor(canvas.width / 15)) - 10;
      y2 = (15 * Math.floor(canvas.height / 15)) - 10;
    });

    // makes square for snake to build off of
    function Square(x, y) {
      this.x = x;
      this.y = y;
    }

    Square.prototype.equals = function(other) {
      return (this.x == other.x) && (this.y == other.y);
    };

    function Snake(initLength) {
      this.body = (function() {
        var ar = [];
        for (let i = 0; i < initLength; i++)
          ar.push(new Square(105 + (i * 15), 105));
        return ar;
      })();

      this.makeFood = function tryagain() {
        function getRandomInt(min, max) { // both inclusive
          return Math.floor(Math.random() * (max - min + 1)) + min;
        }
        while (true) {
          let shouldContinue = false;
          let foodX = 15 * getRandomInt(1, Math.floor(canvas.width / 15) - 2);
          let foodY = 15 * getRandomInt(1, Math.floor(canvas.height / 15) - 2);
          for (let i = 0; i < this.body.length; i++) {
            if (this.body[i].equals(new Square(foodX, foodY))) {
              shouldContinue = true;
              break;
            }
          }
          if (shouldContinue) continue;
          return new Square(foodX, foodY);
        }
      };

      this.food = this.makeFood();

      this.display = function(isDead) {
        c.fillStyle = '#5EF38C';
        for (let sqr of this.body) {
          c.fillRect(sqr.x, sqr.y, 15, 15);
        }
        if (isDead) {
          let hd = this.body[this.body.length - 1];
          c.fillStyle = '#fa34a3';
          c.fillRect(hd.x, hd.y, 15, 15);
        }
        // c.fillStyle = '#9381FF';
        c.fillStyle = '#fa34a3';
        c.fillRect(this.food.x, this.food.y, 15, 15);
      };

      this.update = function() {
        if (moveQueue.length > 0) {
          let hd = this.body[this.body.length - 1];
          let move = moveQueue[0];
          if (moveQueue.length > 1) {
            moveQueue.shift();
          }
          if (move == 39) { // right
            this.body.push(new Square(hd.x + 15, hd.y));
          } else if (move == 37) { // left
            this.body.push(new Square(hd.x - 15, hd.y));
          } else if (move == 38) { // up
            this.body.push(new Square(hd.x, hd.y - 15));
          } else if (move == 40) { // down
            this.body.push(new Square(hd.x, hd.y + 15));
          }
          if (this.body[this.body.length - 1].equals(this.food)) {
            this.food = this.makeFood();
            this.display();
          } else {
            this.body.shift();
            this.display();
          }
        } else
          this.display();
      };

      this.isAlive = function() {
        let hd = this.body[this.body.length - 1];
        if (hd.x > x2 - 20 || hd.x < 15 ||
          hd.y > y2 - 20 || hd.y < 15) {
          return false;
        }
        for (let i = 0; i < this.body.length - 1; i++) {
          if (hd.equals(this.body[i])) {
            return false;
          }
        }
        return true;
      };
    }

    // i is number of "break points in line", wig is factor for wiggle
    function Line(x1, y1, x2, y2, i, wig) {
      this.x1 = x1;
      this.y1 = y1;
      this.x2 = x2;
      this.y2 = y2;
      this.i = i;
      this.wig = wig;
      this.draw = function() {
        c.beginPath();
        c.moveTo(this.x1, this.y1);
        for (let j = 0; j < this.i; j++) {
          var wiggle = (Math.random() - 0.5) * this.wig;
          if (j == this.i - 1)
            wiggle = 0;
          if (x1 == x2) // if vert line
            c.lineTo(this.x1 + wiggle, this.y2 / this.i * (j + 1));
          else // if horizontal line
            c.lineTo(this.x2 / this.i * (j + 1), this.y1 + wiggle);
        }
        c.strokeStyle = "#fa34a3";
        c.stroke();
      };
    }

    // builds a box
    function makeBoundary() {
      var line1 = new Line(x1, y1, x1, y2, 20, 8);
      var line2 = new Line(x2, y1, x2, y2, 20, 8);
      var line3 = new Line(x1, y1, x2, y1, 20, 8);
      var line4 = new Line(x1, y2, x2, y2, 20, 8);
      line1.draw();
      line2.draw();
      line3.draw();
      line4.draw();
    }

    function gameOver(snake) {
      snake.display(true);
      // var audio = new Audio('assets/game-over.wav');
      // audio.play();
      c.fillStyle = "#386FA4";
      c.font = "16px Arial";
      c.fillText("Game Over", canvas.width - 150, 50);
      c.fillText("Score: " + snake.body.length, canvas.width - 150, 70);
      c.fillText("Press 'r' to replay", canvas.width - 150, 90);
      var handler = function again(event) {
        if (event.which == 82) {
          moveQueue = [];
          window.removeEventListener('keydown', handler, false);
          newGame();
        }
      }
      window.addEventListener('keydown', handler, false);
    }

    // set fps
    var fps = 20;
    var now;
    var then = Date.now();
    var interval = 1000 / fps;
    var delta;

    function newGame() {
      snake = new Snake(10);
      // create loop
      function animate() {
        requestAnimationFrame(animate);
        if (spaceBarPressed)
          return
        now = Date.now();
        delta = now - then;
        if (delta > interval) {
          then = now - (delta % interval);
          c.clearRect(0, 0, innerWidth, innerHeight);
          makeBoundary();
          if (moveQueue.length == 0) { // if game hasn't started yet
            c.fillStyle = "#386FA4";
            c.font = "16px Arial";
            c.fillText("Press an arrow key to start!", canvas.width - 240, 50);
          }
          if (snake.isAlive())
            snake.update();
          else
            gameOver(snake);
        }
      }
      animate();
    }
    newGame()
  }
);

function removeDoc(id) {
  var elem = document.getElementById(id);
  return elem.parentNode.removeChild(elem);
}
