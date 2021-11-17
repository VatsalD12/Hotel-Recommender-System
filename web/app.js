const express = require("express");
const app = express();
const cors = require("cors");
const morgan = require("morgan");

app.use("/",express.static("public"));
app.use(express.json());
app.use(express.urlencoded({extended:true}));

app.get("/",async(req,res)=>{
    res.redirect("/login.html")
})

app.use(morgan("dev"));
app.use(cors())
app.listen(8080,()=>{
    console.log("Server running successfullyon port:",8080)
})