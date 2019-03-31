var canvas = document.querySelector('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight - 4;

// lets draw 2d elements
var c = canvas.getContext('2d');
var prevKeyPressed = NaN;
var keyPressed = NaN;

// var snake;
window.addEventListener('keydown',function(event){
  if (keyPressed &&
       ((event.which == 38 && keyPressed != 40) ||
        (event.which == 40 && keyPressed != 38) ||
        (event.which == 37 && keyPressed != 39) ||
        (event.which == 39 && keyPressed != 37))){
          prevKeyPressed = keyPressed;
          keyPressed = event.which;
        }
  else if (!keyPressed && event.which <= 40 && event.which >= 38)
      keyPressed = event.which;
});

window.addEventListener('resize',function(event){
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight - 4;
});

// makes square for snake to build off of
function Square(x, y, dir){
  this.x = x;
  this.y = y;
  this.dir = dir;
  this.equals = function(other){
    return (this.x == other.x) && (this.y == other.y);
  };
}

function Snake(initLength){
  this.body = (function(){
    var ar = [];
    for (let i = 0; i < initLength; i++)
      ar.push(new Square(105 + (i * 15), 105, 'r'));
    return ar;
  })();

  this.makeFood = function tryagain(){
    function getRandomInt(min, max) { // both inclusive
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    while(true){
      let shouldContinue = false;
      let foodX = 15 * getRandomInt(1, Math.floor((canvas.width - 25)/ 15));
      let foodY = 15 * getRandomInt(1, Math.floor((canvas.height - 25 )/ 15));
      for (let i = 0; i < this.body.length; i++){
        if (this.body[i].equals(new Square(foodX, foodY))){
          shouldContinue = true;
          break;
        }
      }
      if (shouldContinue) continue;
      return new Square(foodX, foodY);
    }
  };

  this.food = this.makeFood();

  this.display = function(isDead){
    c.fillStyle = '#ffffff';
    for (let sqr of this.body){
      c.fillRect(sqr.x,sqr.y,15,15);
    }
    if (isDead){
      let hd = this.body[this.body.length - 1];
      c.fillStyle = '#fa34a3';
      c.fillRect(hd.x,hd.y,15,15);
    }
    c.fillStyle = '#fa34a3';
    c.fillRect(this.food.x,this.food.y,15,15);
  };

  this.update = function(){
    if (keyPressed){
      let hd = this.body[this.body.length - 1];
      if (keyPressed == 39){ // right
        this.body.push(new Square(hd.x + 15, hd.y, 'r'));
      }
      else if (keyPressed == 37){ // left
        this.body.push(new Square(hd.x - 15, hd.y, 'l'));
      }
      else if (keyPressed == 38){ // up
        this.body.push(new Square(hd.x, hd.y - 15, 'u'));
      }
      else if (keyPressed == 40){ //down
        this.body.push(new Square(hd.x, hd.y + 15, 'd'));
      }
      if (this.body[this.body.length - 1].equals(this.food)){
        this.food = this.makeFood();
        this.display();
      }
      else {
        this.body.shift();
        this.display();
      }
    }
    else {
      this.display();
    }
  };

  this.isAlive = function(){
    let hd = this.body[this.body.length - 1];
    if (hd.x + 15 > (canvas.width - 10) || hd.x < 15 ||
        hd.y > (canvas.height - 20) || hd.y < 15){
      return false;
    }
    for (let i = 0; i < this.body.length - 1; i++){
      if (hd.equals(this.body[i])){
        return false;
      }
    }
    return true;
  };
}

// i is number of "break points in line", wig is factor for wiggle
function Line(x1, y1, x2, y2, i, wig){
  this.x1 = x1;
  this.y1 = y1;
  this.x2 = x2;
  this.y2 = y2;
  this.i = i;
  this.wig = wig;
  this.draw = function(){
    c.beginPath();
    c.moveTo(this.x1,this.y1);
    for (let j = 0; j < this.i; j++){
      var wiggle = (Math.random() - 0.5) * this.wig;
      if (j == this.i - 1)
        wiggle = 0;
      if (x1 == x2) // if vert line
          c.lineTo(this.x1 + wiggle, this.y2/this.i * (j + 1));
      else // if horizontal line
        c.lineTo(this.x2/this.i * (j + 1), this.y1 + wiggle);
    }
    c.strokeStyle = "#fa34a3";
    c.stroke();
  };
}

// builds a box
function makeBoundary(){
  var line1 = new Line(10, 10, 10, canvas.height - 10, 20, 8);
  var line2 = new Line(canvas.width - 10, 10,
    canvas.width - 10, canvas.height - 10, 20, 8);
  var line3 = new Line(10, 10, canvas.width - 10, 10, 20, 8);
  var line4 = new Line(10, canvas.height - 10, canvas.width - 10,
    canvas.height - 10, 20, 8);
  line1.draw();
  line2.draw();
  line3.draw();
  line4.draw();
}

function gameOver(snake){
  snake.display(true);
  // var audio = new Audio('assets/game-over.wav');
  // audio.play();
  c.fillStyle = "#386FA4";
  c.font = "16px Arial";
  c.fillText("GAME OVER", canvas.width - 150, 50);
  c.fillText("Score: " + snake.body.length, canvas.width - 150, 70);
  c.fillText("Press 'r' to replay", canvas.width - 150, 90);
  var handler = function again(event){
    if (event.which == 82){
      keyPressed = NaN;
      window.removeEventListener('keydown', handler, false);
      newGame();
    }
  }
  window.addEventListener('keydown',handler, false);
}

// set fps
var fps = 30;
var now;
var then = Date.now();
var interval = 1000/fps;
var delta;
snake = new Snake(10);
function newGame(){
  snake = new Snake(10);
  // create loop
  function animate(){
    requestAnimationFrame(animate);
    now = Date.now();
    delta = now - then;
    if (delta > interval) {
      then = now - (delta % interval);
      c.clearRect(0,0,innerWidth,innerHeight);
      makeBoundary();
      if (!keyPressed){ // if game hasn't started yet
        c.fillStyle = "#386FA4";
        c.font = "16px Arial";
        c.fillText("Press an arrow key to start!", canvas.width - 240, 50);
      }
      if (snake.isAlive()){
        let hd = snake.body[snake.body.length - 1];
        if (!((keyPressed == "39" && hd.dir == "l") ||
            (keyPressed == "37" && hd.dir == "r") ||
            (keyPressed == "40" && hd.dir == "u") ||
            (keyPressed == "38" && hd.dir == "d"))){
          snake.update();
        } else {
          keyPressed = prevKeyPressed;
          snake.update();
        }
      }
      else{
        gameOver(snake);
      }
    }
  }
  animate();
}
newGame();
