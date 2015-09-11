//机器学习之决策树算法

//熵，用来表示信息集合的纯度，熵值越低，信息纯度越高。信息论的一种解释是，熵确定了要编码集合S中任意一个成员所需的二机制数。
// Entropy(S) = - p+ log2 p+  -  p_ log2 p_
// 例如一个S集合有14个实例，9正例，5个反例, 根据公式

//自顶向下的贪婪搜索可能的决策树空间构造一颗决策树，ID3
//


var entropy = function(examples) {
	var total = samples.length;
	var wellSmaples = samples.filter(function(item) {
		return item.output == 1;
	});

	var wellCount = wellSmaples == undefined ? 0 : wellSmaples.length;

	var badCount = total - wellCount;

	return -(wellCount / total) * log(2, wellCount / total) - (badCount / total) * log(2, badCount / total);
}

//ID3(Examples, Target_attribute, Attributes)
//Target_attribute 是决策树预测是使用的属性，Attributes是供决策树测试的属性列表。 返回能正确分类Examples的决策树
//创建树的Root节点
//如果
//	Examples都为true，那么返回lable=+的单节点树Root
//	Examples都为false，那么返回lable=-的单节点树Root
//	Attributes为空，那么返回单节点树root，lable = Examples 中最普遍的Target_attribute值
//否则
//	Root的决策属性A = Attributes中分类Examples能力最好的属性
//	对于A的每一个可能值vi在Root下加一个新的分支预测examples(vi)
//		如果 Examples(vi) 为空	，在新分支加一个叶子节点，节点的lable = Examples中最普遍的Target_attribute值
//		否则 在这个新分支下加一个子树ID3（Examples(vi), Target_attribute,Attributes(A)）
//结束 

var buildDecisionTree = function(examples, target_attributes, attributes) {
	//创建决策树根，默认是一个非叶子的节点
	var root = {
		leaf: false
	};
	//如果Examples的target_attribute相同，返回一个叶子节点
	for (var index = 0; index < target_attributes.length; index++) {
		if (ArrayList.filter(target_attributes[index], examples).length == examples.length) {
			root.leaf = true;
			root.label = target_attributes[index].value;
			return root;
		}
	}

	if (attributes.length == 0) {
		root.leaf = true;
		root.label = ArrayList.mostCommonTargetAttributeName(target_attributes, examples).value;
		return root
	}
	//选择Attributes中分类Examples能力最好的属性作为root的决策属性
	root.attribute = ArrayList.magicAttribute(attributes, examples);
	root.children = [];
	var optionsOfSpecificAtrribute = attributes.filter(function(item) {
		return item.name == root.attribute;
	}).pop().value;

	//为每个option对应的examplesWithSpecificOption建立一个分支
	for (var index in optionsOfSpecificAtrribute) {
		var option = optionsOfSpecificAtrribute[index];
		var examplesWithSpecificOption = examples.filter(function(example) {
			if (option instanceof Interval) {
				return option.contains(example[root.attribute]);
			} else
				return option == example[root.attribute];
		});
		//如果examplesWithSpecificOption集合为空，分支为一个叶子节点
		if (examplesWithSpecificOption.length == 0) {
			var node = {
				leaf: true
			};
			node.label = ArrayList.mostCommonTargetAttributeValue(target_attributes, examples).value;
			root.children.push(node);
		} else {
			var attrs = attributes.filter(function(attribute) {
				return attribute.name != root.attribute;
			});
			//将examplesWithSpecificOption用除了root.attribute之外的其他属性来构建子树，作为root的分支
			root.children.push(buildDecisionTree(examplesWithSpecificOption, target_attributes, attrs));
		}
	};

	return root;
}

var ArrayList = {};

//在attributes中找到一个最能分类examples的属性
ArrayList.magicAttribute = function(attributes, examples) {
	return attributes[0].name;
}

// 这个一个属性列表，包含名称和对应的值， 这些值可以是离散，也可能是连续的，连续的值可以用一个interval object来表示
var Interval = (function() {
	function Interval(from, to) {
		this.from = from;
		this.to = to;
	}
	Interval.of = function(from, to) {
		return new Interval(from, to);
	}
	//用来判断某个离散的值，是否属于这个区间
	Interval.prototype.contains = function(value) {
		return value > this.from && value <= this.to;
	}
	return Interval;
})();

// 样例包含的所有属性和属性的取值
var attributes = [{
	name: 'outlook',
	value: ['sunny', 'overcast', 'rain']
}, {
	name: 'temperature',
	value: [Interval.of(0, 50), Interval.of(50, 60), Interval.of(60, 70), Interval.of(70, 80), Interval.of(80, 90), Interval.of(90, 100)]
}, {
	name: 'humidity',
	value: [Interval.of(0, 50), Interval.of(50, 60), Interval.of(60, 70), Interval.of(70, 80), Interval.of(80, 90), Interval.of(90, 100)]
}, {
	name: 'windy',
	value: [true, false]
}];

ArrayList.filter = function(condition, source) {
	return source.filter(function(item) {
		return item[condition.name] == condition.value
	});
}

var target_attributes = [{
	name: 'play',
	value: true
}, {
	name: 'play',
	value: false
}];

ArrayList.mostCommonTargetAttributeValue = function(attributes, examples) {
	return target_attributes.reduce(function(result, item) {
		if (ArrayList.filter(result, examples).length > ArrayList.filter(item, examples).length) {
			return result;
		} else {
			return item;
		}
	});
}



//准备一组14个样例，样例来自维基百科决策树
var examples = [{
	outlook: "sunny",
	temperature: 85,
	humidity: 85,
	windy: false,
	play: false
}, {
	outlook: "sunny",
	temperature: 80,
	humidity: 90,
	windy: true,
	play: false
}, {
	outlook: "overcast",
	temperature: 83,
	humidity: 78,
	windy: false,
	play: true
}, {
	outlook: "rain",
	temperature: 70,
	humidity: 96,
	windy: false,
	play: true
}, {
	outlook: "rain",
	temperature: 68,
	humidity: 80,
	windy: false,
	play: true
}, {
	outlook: "rain",
	temperature: 65,
	humidity: 70,
	windy: true,
	play: false
}, {
	outlook: "overcast",
	temperature: 64,
	humidity: 65,
	windy: true,
	play: true
}, {
	outlook: "sunny",
	temperature: 72,
	humidity: 95,
	windy: false,
	play: false
}, {
	outlook: "sunny",
	temperature: 69,
	humidity: 70,
	windy: false,
	play: true
}, {
	outlook: "rain",
	temperature: 75,
	humidity: 80,
	windy: false,
	play: true
}, {
	outlook: "sunny",
	temperature: 75,
	humidity: 70,
	windy: true,
	play: true
}, {
	outlook: "overcast",
	temperature: 72,
	humidity: 90,
	windy: true,
	play: true
}, {
	outlook: "overcast",
	temperature: 81,
	humidity: 90,
	windy: true,
	play: true
}, {
	outlook: "rain",
	temperature: 71,
	humidity: 80,
	windy: true,
	play: false
}]


// 对数基变换公式  logx(y) =  ln(y)/ln(x)

var log = function(base, x) {
	return Math.log(x) / Math.log(base);
}

var S = [{
	"output": 1
}, {
	"output": 1
}, {
	"output": 1
}, {
	"output": 1
}, {
	"output": 1
}, {
	"output": 1
}, {
	"output": 1
}, {
	"output": 1
}, {
	"output": 1
}, {
	"output": -1
}, {
	"output": -1
}, {
	"output": -1
}, {
	"output": -1
}, {
	"output": -1
}];



// var Sample = (function() {
//     function Sample(input, output) {

//     }

//     return Sample;

// }());