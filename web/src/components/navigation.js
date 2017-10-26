import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from 'react-dom';

import { Nav, Navbar, NavBrand, NavItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';


export class FSNav extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedItem: this.props.pages[0]
        };
    }

    handleSelect(selectedKey) {
        this.setState({
            selectedItem: this.props.pages.filter((page) => page.slug == selectedKey)[0]
        });
    }

    render() {
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
}

FSNav.propTypes = {
    pages: PropTypes.arrayOf(PropTypes.object)
};
