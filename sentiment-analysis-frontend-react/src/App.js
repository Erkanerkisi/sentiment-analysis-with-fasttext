import './App.css';
import {useEffect, useState} from "react";
import {Row, Container, Col, InputGroup, FormControl} from 'react-bootstrap';
import axios from "axios";


function App() {

    const [text, setText] = useState("");
    const [response, setResponse] = useState("");

    useEffect(() => {
        let timeOutId;
        if (text !== "") {
            timeOutId = setTimeout(() => predict(text), 3000);
        }
        return () => {
            if(timeOutId != null) {
              clearTimeout(timeOutId)
            }
        };
    }, [text]);

    const predict = (text) => {
        axios.post('http://localhost:105/prediction', {
            text: text,
        })
            .then(function (response) {
                console.log(response)
                setResponse(response.data)
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    return (
        <div className="App">
            <Container>
                <Row className="align-items-center">
                    <Col>
                        <InputGroup>
                            <InputGroup.Text>Input</InputGroup.Text>
                            <FormControl as="textarea"
                                         aria-label="With textarea"
                                         onChange={(e) => setText(e.target.value)}
                            />
                        </InputGroup>
                    </Col>
                    <Col>{response}</Col>
                </Row>
            </Container>
        </div>
    );
}

export default App;
