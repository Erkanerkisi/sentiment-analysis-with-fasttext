import './App.css';
import {useEffect, useState} from "react";
import {Row, Container, Col, InputGroup, FormControl} from 'react-bootstrap';


function App() {

    const [text, setText] = useState("");

    useEffect(() => {
        let timeOutId;
        if (text != null || text !== "") {
            timeOutId = setTimeout(() => console.log("trigger api call" + text), 3000);
        }
        return () => {
            if(timeOutId != null) {
              clearTimeout(timeOutId)
            }
        };
    }, [text]);

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
                    <Col>{text}</Col>
                </Row>
            </Container>
        </div>
    );
}

export default App;
