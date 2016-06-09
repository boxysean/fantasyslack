import React from 'react';
import ReactDOM from 'react-dom';

import { Nav, Navbar, NavBrand, NavItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';


export var FSNav = React.createClass({
    propTypes: {
        pages: React.PropTypes.arrayOf(React.PropTypes.object)
    },

    getInitialState: function() {
        return {
            selectedItem: this.props.pages[0]
        }
    },

    handleSelect: function(selectedKey) {
        this.setState({
            selectedItem: this.props.pages.filter((page) => page.slug == selectedKey)[0]
        });
    },

    render: function() {
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>Fantasy Slack</Navbar.Brand>
                </Navbar.Header>
                <Nav activeKey={this.state.selectedItem.slug} onSelect={this.handleSelect}>
                    {this.props.pages.map((page) => {
                        if (page.app !== undefined) {
                            return (
                                <LinkContainer to={'/' + page.slug}>
                                    <NavItem eventKey={page.slug}>{page.name}</NavItem>
                                </LinkContainer>);
                        } else {
                            return <NavItem eventKey={page.slug} disabled={true}>{page.name}</NavItem>;
                        }
                    })}
                </Nav>
            </Navbar>
        )
    }
});

