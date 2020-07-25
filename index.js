const express = require('express');
const path = require('path');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();
const detectRoute = require('./routes/detect.route');


const {
    notFound,
    errorHandler
} = require('./middlewares');

const app = express();


app.use(morgan("dev"));
app.use(cors());
app.use(helmet());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use('/static/uploads', express.static(path.join(__dirname, 'public/uploads')));
app.use('/', express.static(path.join(__dirname, 'public/output')));
app.get('/', (req, res) => {
    res.json({
        "Message": "Hello from server"
    })
})
app.use('/api/v1', detectRoute)
//HANDLE ERROR
app.use(notFound)
app.use(errorHandler)
const PORT = process.env.PORT || 80

app.listen(PORT, () => { console.log(`Server started on port ${PORT}`) })