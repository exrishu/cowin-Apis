## Cowin-Extended-Api

<h4>Purpose:</h4>To return the avaliable slots for the given pincode,date and age group in request.<br>
<h4>Launguage:</h4>Python,Flask,SqlAlchemy,Heroku PostgreSQL.<br>
<h4>Implementation:</h4> 1.Create a virtual env in your system.<br>2.Clone the reposirtory inside your venv project folder.<br>3.Run the project and install required modules.<br>4.Generate a token by passing username in request param by using END point (/user/generate/token).<br>5.Add <i>'x-access-token'</i> in the header of the request to return the data.<br>6.Use END-point(/api/v1/get/vaccine/slots/all_age) to return  the response of the given request.<br>

## Sample
#### Request:

<pre><code>{
    "pincode": "228001",
    "date": "26-07-2021",
    "age":"18+" 
}</code></pre>

#### Add header as shown below(point no.5)
![jwt](https://user-images.githubusercontent.com/19299841/127103328-e53809b1-4d92-486c-aa59-c3e992b0523b.png)

#### Response:

<pre><code>{
    "slots": [
        {
            "dose1": 0,
            "dose2": 6,
            "max_age": 80,
            "min_age": 18,
            "place": "DMH Ayush Wing COVAXIN",
            "vaccine": "COVAXIN"
        },
        {
            "dose1": 0,
            "dose2": 5,
            "max_age": 80,
            "min_age": 18,
            "place": "Bhadaiyan CHC",
            "vaccine": "COVISHIELD"
        }
    ]
}</code></pre>
