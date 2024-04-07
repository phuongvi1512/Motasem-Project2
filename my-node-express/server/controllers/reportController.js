const mysql = require('mysql2');

// Connection Pool
let connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME
});

// View Reports
exports.view = (req, res) => {
    // User the connection
    connection.query('SELECT * FROM reports ', (err, rows) => {
      // When done with the connection, release it
      if (!err) {
        let removedReport = req.query.removed;
        res.render('home', { rows, removedReport });
      } else {
        console.log(err);
      }
      console.log('The data from report table: \n', rows);
    });
  }

  // Add new report

exports.form = ( req, res ) => {
  res.render('add-report');
}
exports.create = (req, res) => {
    const { trace_id, file_id, switch_id, timestamp, file_size } = req.body;
    let searchTerm = req.body.search;
  
    // User the connection
    connection.query('INSERT INTO reports SET trace_id = ?, file_id = ?, switch_id = ?, timestamp = ?, file_size = ?', [trace_id, file_id, switch_id, timestamp, file_size], (err, rows) => {
      if (!err) {
        res.render('add-report', { alert: 'Report added successfully.' });
      } else {
        console.log(err);
      }
      console.log('The data from report table: \n', rows);
    });
  }
  