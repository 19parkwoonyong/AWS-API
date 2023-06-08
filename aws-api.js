//import required packages

var AWS = require('aws-sdk');

//AWS access details
AWS.config.update({
    accessKeyId: '',
    secretAccessKey: '',
    region: 'ap-northeast-2'
});

//input parameters
var params = {
    Image: {
        S3Object: {
            Bucket: "zerash",
            Name: "uk.JPG"
        }
    },
    MaxLabels: 10,
    MinConfidence: 70
};

//Call AWS Rekognition Class
const rekognition = new AWS.Rekognition();

rekognition.detectLabels(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else console.log(data);           // successful response
});

// end code
