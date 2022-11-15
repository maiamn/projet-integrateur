export default class APIService{
    static sendToServer(body){
        return fetch('http://localhost:5000/sent',
        
        {
            credentials: "include",
            'method':'POST',
             headers : {
            'Content-Type':'application/json'
      },
      body:JSON.stringify(body)
    })
    .then(response1 => response1.json())
    .catch(error => console.log(JSON.stringify(body) + error))
    }

}