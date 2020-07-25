const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const app = express()

app.use(cors())
app.use(helmet())
app.use(morgan("dev"))
app.get("/", (req, res) => {
    res.json({
        "Message": "Hello from server"
    })
})
const PORT = process.env.PORT || 5000

app.listen(PORT, () => { console.log(`Server started on port ${PORT}`) })