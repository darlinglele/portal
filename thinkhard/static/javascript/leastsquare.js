var LeastSquare = {};
function LinearRegression(coordinate) {
	
	this.leastSquare = function() {
		var features = coordinate.points.map(function(item) {
		return {
			x: (item.x),
			y: (item.y)
		};});

		var n = features.length;
		var xa = 0;
		var ya = 0;
		for (var i = 0; i < n; i++) {
			xa += features[i].x;
			ya += features[i].y;
		};
		xa /= n;
		ya /= n;

		var xx = 0;
		var yy = 0;
		var xy = 0;
		for (var i = 0; i < n; i++) {
			var tmpx = features[i].x - xa;
			var tmpy = features[i].y - ya;
			xx += tmpx * tmpx;
			yy += tmpy * tmpy;
			xy += tmpx * tmpy;

		};
		var m_b = xy / xx;
		var m_a = ya - m_b * xa;
		coordinate.drawLine(m_b, -1, m_a);		
	}

}
function createPoints() {
	var points = [];
	for (var i = 0; i < 600; i += 10) {
		points.push({
			x: i,
			y: 0.2 * i + Math.random() * 50,
			color: "red",
			size: 5
		});
	};
	return points;
}

var FEATURES = createPoints().map(function(item) {
	return {
		x: [1, item.x],
		y: (item.y)
	};
})


var leastCoordinate= new Coordinate("leastsquare");

var linearRegression = new LinearRegression(leastCoordinate);

leastCoordinate.add(createPoints());
linearRegression.leastSquare();

LeastSquare.clear = function() {
    leastCoordinate.points =[];
	leastCoordinate.clear();
}

LeastSquare.calculate = function() {
	var linearRegression = new LinearRegression(leastCoordinate);
	leastCoordinate.refresh();
	linearRegression.leastSquare();
}