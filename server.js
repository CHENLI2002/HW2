const express = require("express");
const app = express();
const {Datastore} = require("@google-cloud/datastore");
const port = 8080;
const datastore = new Datastore();

app.use(express.json());

app.get("/greeting", (req, res) => {
    res.setHeader("Content-Type", "text/html");
    res.send(`<!DOCTYPE html><html><body><h1>Hello, World!</h1></body></html>`);
});

app.post("/register", async (req, res) => {
    const username = req.body.username;
    const userKey = datastore.key(["User", username]);
    await datastore.save({
        key: userKey,
        data: {
            username: username,
        },
    });
    res.status(200).json({ message: "User registered successfully" });
});

app.get("/list", async (req, res) => {
    const query = datastore.createQuery("User");
    const [users] = await datastore.runQuery(query);
    const userNames = users.map((user) => user.username);
    res.status(200).json({"users": userNames});
});


app.post("/clear", async (req, res) => {
    const query = datastore.createQuery("User");
    const [users] = await datastore.runQuery(query);
    const keys = users.map((user) => user[Datastore.KEY]);
    if (keys.length > 0) {
      await datastore.delete(keys);
    }
    res.status(200).json({ message: "Cleared" });
});
  

const server = app.listen(port, '0.0.0.0', () => {
    console.log(`Server is running on port ${port}`);
});

server.ref();
process.stdin.resume();

process.on("SIGINT", () => {
    server.close(() => process.exit(0));
});