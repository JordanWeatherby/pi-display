import React from 'react';
import Nav from './Nav';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import Log from './Log';
import { Container } from 'react-bulma-components';
import SendMessageForm from './SendMessageForm';

const Dashboard = () => {
    return (
        <Router>
            <Nav />
            <div className="pl-3 pr-3">
                <Container breakpoint="desktop">
                    <Routes>
                        <Route exact path='/' element={<HomePage />}/>
                        <Route exact path='/send-message' element={<SendMessageForm />}/>
                        <Route path='/*' element={<Log />}/>
                    </Routes>
                </Container>
            </div>
        </Router>
    );
};

export default Dashboard;
