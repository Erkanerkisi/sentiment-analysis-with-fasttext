import './App.css';
import {useEffect, useState} from "react";
import {Button, Row, Container, Col, InputGroup, FormControl, Form} from 'react-bootstrap';
import axios from "axios";
import {EmojiSmile, EmojiNeutral, EmojiAngry} from 'react-bootstrap-icons';

function App() {

    const [text, setText] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);
    const [actualResult, setActualResult] = useState(-1);

    useEffect(() => {
        let timeOutId;
        if (text !== "") {
            setLoading(true)
            timeOutId = setTimeout(() => predict(text), 3000);
        }
        return () => {
            if (timeOutId != null) {
                setLoading(false)
                clearTimeout(timeOutId)
            }
        };
    }, [text]);

    const predict = async (text) => {
        axios.post('http://localhost:105/prediction', {
            text: text,
        })
            .then(function (response) {
                console.log(response)
                setResponse(response.data)
                setLoading(false)
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    const convertResponseToIcon = (data) => {
        if (loading)
            return "Loading"
        if (data === "__label__1") {
            return <EmojiSmile size={150} color="green"/>
        } else if (data === "__label__0") {
            return <EmojiAngry size={150} color="red"/>
        } else if (data === "__label__2") {
            return <EmojiNeutral size={150} color="grey"/>
        }
    }

    const send = () => {
        axios.get('http://localhost:105/send-data')
            .then(function (response) {
                console.log(response)
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    const refreshModel = () => {
        axios.get('http://localhost:105/refresh-model')
            .then(function (response) {
                console.log(response)
            })
            .catch(function (error) {
                console.log(error);
            });
    }


    return (
        <div>
            <br/><br/><br/><br/><br/>
            <Container>
                <Row className="align-items-center">
                    <Col>
                        <InputGroup>
                            <InputGroup.Text>Input</InputGroup.Text>
                            <FormControl as="textarea"
                                         rows={10}
                                         aria-label="With textarea"
                                         onChange={(e) => setText(e.target.value)}
                            />
                        </InputGroup>
                    </Col>
                    <Col>{convertResponseToIcon(response)}</Col>
                </Row>
                <br/><br/><br/>
                <Row>
                    <Form.Group className="mb-3" controlId="formBasicCheckbox">
                        <Form.Check checked={actualResult === 1} type="checkbox" label="Olumlu"
                                    onChange={() => setActualResult(1)}/>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBasicCheckbox">
                        <Form.Check checked={actualResult === 0} type="checkbox" label="Nötr"
                                    onChange={() => setActualResult(0)}/>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBasicCheckbox">
                        <Form.Check checked={actualResult === 2} type="checkbox" label="Olumsuz"
                                    onChange={() => setActualResult(2)}/>
                    </Form.Group>
                    <Button disabled={actualResult === -1} onClick={() => send(actualResult)}>Data Setine
                        Gönder</Button>
                </Row>
                <br/>
                <Row>
                    <Button onClick={() => refreshModel()}>Refresh model</Button>
                </Row>
            </Container>
        </div>
    );
}

export default App;
