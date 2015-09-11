function scaleFeatures(features) {
    // x = x- mean(x)/ max(x) -min(x)
    var max = [0, 0];
    var min = [0, 1000000];
    var mean = [0, 0];
    var maxY = 0;
    var meanY = 0;
    var minY = 10000;
    var length = features.length;
    for (var i = 0; i < length; i++) {
        feature = features[i];
        for (var j = 0; j < feature.x.length; j++) {
            max[j] = feature.x[j] > max[j] ? feature.x[j] : max[j];
            min[j] = feature.x[j] < min[j] ? feature.x[j] : min[j];
            mean[j] += feature.x[j] / length;
        };
        maxY = feature.y > maxY ? feature.y : maxY;
        minY = feature.y < minY ? feature.y : minY;
        meanY += feature.y / length;
    }
    for (var i = 0; i < length; i++) {
        feature = features[i];
        for (var j = 1; j < feature.x.length; j++) {
            feature.x[j] = (feature.x[j] - mean[j]) / (max[j] - min[j])
        };
        // feature.y = (feature.y- meanY)/ (maxY - minY);
    };
    return features;
}