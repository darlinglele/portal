Float64Array.copy = function(from) {
	var to = new Float64Array(new ArrayBuffer((from.length) * 8));
	for (var i = 0; i < from.length; i++) {
		to[i] = from[i];
	}
	return to;
}

function GradientDescent(features, coordinate) {
	var theta = new Float64Array(new ArrayBuffer((features[0].x.length) * 8));
	for (var i = 0; i < theta.length; i++) {
		theta[i] = 5;
	};
	// var MAX = features.length*10000;
	var MAX = features.length;
	var alpha = 0.000001;
	// console.log(MAX * alpha);

	var M = features.length; // 训练数据的个数
	var J = theta.length; // 回归系数的维度

	// 假设回归系数theta的预测分数
	var h = function(theta, feature) {
		var y = 0;
		for (var i = 0; i < feature.x.length; i++) {
			y = y + (theta[i] * feature.x[i]);
		};
		return y;
	}
	//损失函数
	var cost = function(theta, features) {
		var result = 0;
		for (var i = 0; i < features.length; i++) {
			var d = (h(theta, features[i]) - features[i].y);
			result += d * d;
		};
		return result / (2 * features.length);
	}

	this.descent = function() {
		for (var i = 0; i < MAX; i++) {
			var y = features[i % M].y;
			var x = features[i % M].x;
			var lastTheta = Float64Array.copy(theta);
			var maxDistance = 0;

			var d = cost(theta, features);

			coordinate.add({
				x: (i / MAX) * coordinate.width,
				y: (d / 1500000) * coordinate.height,
				size: 2,
				color: "blue"
			});
			for (var j = 0; j < J; j++) {
				var guess = h(lastTheta, features[i % M]);
				theta[j] = theta[j] - alpha * (guess - y) * x[j];
			};
			if (i % (MAX / 10) == 0) {
				coordinate.drawLine(theta[1], -1, theta[0], "pink");
			}
		}
		coordinate.drawLine(theta[1], -1, theta[0]);
		console.log(theta);
		console.log(cost(theta, features))
	}

	this.getValue = function(obj) {
		var theta = this.getTheta();
		var val = 0;
		for (var i = 0; i < theta.length; i++) {
			val += theta[i] * obj[i];
		};
		return val;
	}


	this.getTheta = function() {
		return theta;
	}
}

var length = 600;

function createPoints() {
	var points = [];
	for (var i = 0; i < length; i += 10) {
		points.push({
			x: i,
			y: i * 0.12 + Math.random() * 20,
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
//(面积,房间数量,离地铁距离)
var datasets = [{
	x: [1, 100, 3, 1],
	y: 300
}, {
	x: [1, 110, 3, 1],
	y: 330
}, {
	x: [1, 120, 3, 1],
	y: 360
}, {
	x: [1, 150, 3, 1],
	y: 450
}, {
	x: [1, 150, 4, 1],
	y: 460
}, {
	x: [1, 150, 2, 1],
	y: 430
}, {
	x: [1, 150, 5, 1],
	y: 470
}, {
	x: [1, 100, 2, 1],
	y: 290
}, {
	x: [1, 100, 4, 1],
	y: 310
}, {
	x: [1, 100, 2, 2],
	y: 280
}, {
	x: [1, 100, 2, 3],
	y: 275
}, {
	x: [1, 100, 2, 4],
	y: 270
}, {
	x: [1, 100, 2, 5],
	y: 250
}]



var gradientCoordinate = new Coordinate("gradientdescent");

var gradientDescent = new GradientDescent(FEATURES, gradientCoordinate);

gradientCoordinate.add(createPoints());

gradientDescent.descent();
// regression.drawLine(1,1,3);
// linearRegresion.descend();
// for (var i = 0; i < datasets.length; i++) {
// 	console.log(datasets[i].y +':'+ linearRegresion.getValue(datasets[i].x));
// };