/**
 * Version: 14/Dec/2018
 * Author: Killian O'Dálaigh
 * Description: Creates a AID for the user and pushes the User object to the
 * DynamoDB Table AccountDetails
 */
 
const AWS = require('aws-sdk'); // Aws sdk
const UUID = require('uuid/v1'); // UUID generator
const bcrypt = require('bcrypt'); // Encryption libraryS
const docClient = new AWS.DynamoDB.DocumentClient(); // DynamoDB client
const table = process.env.TABLE; // Global const TABLE

exports.handler = (event, context, callback) => { // event comes is in JSON
    console.log(JSON.stringify(event, null, 2));
    //console.log(JSON.stringify(event.UserName));
    //console.log(JSON.stringify(event.Password));
    
    // Change to UNIQUE ID
    const saltRounds = 10; // Salt rounds for encryption
    const AID = UUID();
    const password = '';
    const username = '';
    const email = '';
    const phoneNum = '';
    
    
    bcrypt.hash(event.Password, saltRounds, function(err, hash) {
        password = hash;
    }, function(err, data) {console.log(err);} );

    bcrypt.hash(event.UserName, saltRounds, function(err, hash) {
        username = hash;
    }, function(err, data) {console.log(err);} );

    bcrypt.hash(event.Email, saltRounds, function(err, hash) {
        email = hash;
    }, function(err, data) {console.log(err);} );

    bcrypt.hash(event.PhoneNum, saltRounds, function(err, hash) {
        phoneNum = hash;
    }, function(err, data) {console.log(err);} );

        docClient.put({
            TableName: table,
            Item: {
                "AID":AID,
                "UserName":username,
                "Password":password,
                "Email": email,
                "Phone": phoneNum
            }
        }, function(err, data) {
            if (err) {
                console.log(err);
                callback(err, err);
            } 
            else console.log("DynamoDB write succeeded with: ", data);
        });
    callback(null, AID);
};