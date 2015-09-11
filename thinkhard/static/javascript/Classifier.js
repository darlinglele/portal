var Classifier = (function() {
    'use strict';
    Classifier = function(arg) {
        var calculation = 0;
        var intervalObject;
        var interval;
        var inprocess;
        var coordinate;
        var callback;
        var weights;
        var samples;
        var alpha = 0.5;

        this.setAlpha = function(val){
            alpha =val;
        }

        this.stop = function(callback, reason) {
            var reason = reason || {
                "message": "stopped by client"
            };
            clearInterval(intervalObject);

            inprocess = false;

            return callback != null ? callback(reason) : null;
        };

        this.setInterval = function(time) {
            clearInterval(intervalObject);
            interval = time;
            if (!inprocess) {
                return;
            }

            var classifier = this;
            if (time == 0) {
                while (true) {
                    if (correct()) {
                        inprocess = false;
                        callback({
                            message: "done"
                        });
                        return;
                    }

                }
            }

            intervalObject = setInterval(function() {
                if (correct()) {
                    var reason = {
                        message: "done"
                    };
                    stop(callback, reason);
                }
            }, time);
        };


        var check = function(input, weights) {
            var sum = 0;
            for (var i = 0; i < input.length; i++) {
                sum += input[i] * weights[i];
            }
            sum += 1 * weights[weights.length - 1];
            return sum > 0 ? 1 : -1;
        }

        var correct = function() {
            coordinate.refresh();
            var dismatch = false;
            samples.forEach(function(sample) {
                var result = check(sample.input, weights);
                if (result != sample.output) {
                    for (var i = 0; i < weights.length - 1; i++) {
                        weights[i] += alpha * sample.output * sample.input[i];
                    };
                    dismatch = true;
                    weights[weights.length - 1] += alpha * sample.output;
                }

            });

            calculation++;
            coordinate.drawLine(weights[0], weights[1], weights[2]);
            return !dismatch;
        };


        this.process = function(samples2, coordinate2, callback2) {
            samples = samples2 || [];
            if (!samples.length) {
                return;
            }
            callback = callback2;
            coordinate = coordinate2;
            weights = new Float32Array(new ArrayBuffer((samples[0].input.length + 1) * 4));

            calculation++;

            inprocess = true;

            this.setInterval(interval);
        };
    };


    return Classifier;

}());