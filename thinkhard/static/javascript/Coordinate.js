   var Coordinate = (function() {

       function Coordinate(canvas) {
           this.canvas = document.getElementById(canvas);
           this.cxt = this.canvas.getContext("2d");
           this.width = this.canvas.width;
           this.height = this.canvas.height;
           this.scale = 20;
           this.isShow = true;
           this.points = [];
           this.pointStyle = {
               color: "red",
               size: 5
           };

           this.origin = {
               "x": 0,
               "y": this.canvas.height
           };

           this.clear();
           var coordinate = this;
           this.canvas.addEventListener('mousemove', function(evt) {
               var mousePos = getMousePos(coordinate.canvas, evt);
               var message = 'x: ' + mousePos.x + ', y:' + (coordinate.canvas.height - mousePos.y);
               writeMessage(coordinate.canvas, message);
           }, false);

           this.canvas.addEventListener('mouseout', function(evt) {
               var message = 'x: 0.00, y: 0.00';
               writeMessage(coordinate.canvas, message);
           }, false);

           this.canvas.addEventListener('click', function(evt) {
               var mousePos = getMousePos(this, evt);
               coordinate.add({
                   x: mousePos.x,
                   y: coordinate.origin.y - mousePos.y,
                   color: coordinate.pointStyle.color,
                   size: coordinate.pointStyle.size
               });
           }, false);

           function writeMessage(canvas, message) {
//               var context = canvas.getContext('2d');
//                              context.clearRect(1, 1, 81, 30);
//                              context.font = '9pt Calibri';
//                              context.fillStyle = 'black';
//                              context.fillText(message, 10, 25);
           }


           function getMousePos(canvas, evt) {
               var rect = canvas.getBoundingClientRect();
               return {
                   x: evt.clientX - rect.left,
                   y: evt.clientY - rect.top
               };
           }
       }

       Coordinate.prototype.add = function(obj) {
            var coordinate =this;
           if (obj instanceof Array) {
                obj.forEach(function(item,index){
                    coordinate.add(item);
                });
           } else {
               this.points.push(obj);
               this.drawPoint(obj);
           }
       }


       Coordinate.prototype.drawPoint = function(point) {
           this.cxt.fillStyle = point.color;
           this.cxt.fillRect(point.x - point.size / 2, this.origin.y - point.y - point.size / 2, point.size, point.size);
       };

       Coordinate.prototype.refresh = function() {
           this.clear();
           for (var i = 0; i < this.points.length; i++) {
               this.drawPoint(this.points[i]);
           }
       };

       Coordinate.prototype.drawLine = function(a, b, c, color) {
           this.cxt.beginPath();
           this.cxt.moveTo(0, this.origin.y - (-c / b));
           this.cxt.lineTo(this.canvas.width, this.origin.y - (-(a / b) * this.canvas.width - c / b));
           if(color!=undefined){
            this.cxt.strokeStyle = color;
           }
           else{
            this.cxt.strokeStyle = "black";
           }
           this.cxt.stroke();
       };

       Coordinate.prototype.clear = function() {
           this.cxt.clearRect(0, 0, this.canvas.width, this.canvas.height);

           this.cxt.beginPath();
           this.cxt.moveTo(0, this.canvas.height);
           this.cxt.lineTo(this.canvas.width, this.canvas.height);

           this.cxt.moveTo(0, this.origin.y);
           this.cxt.lineTo(0, 0);
           this.cxt.stroke();
       }
       return Coordinate;
   })();