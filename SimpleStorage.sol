// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {

    uint256 private age;
    string public name;
    mapping(string => uint256) public people;

    function setName(string memory _name, uint256 _age) public{
        name = _name;
        age = _age;
        people[_name] = _age;
    }

    function getInfo() public view returns (uint256, string memory){
        return (age, name);
    }

}
