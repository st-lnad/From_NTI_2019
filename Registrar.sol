pragma solidity >=0.4.22 <0.6.0;



contract Registrar {
    address public owner;


    struct request_struc{
        string number;
        string timestamp;
        bool isAdd;
    }

    struct accounts_struc{
        string number;
        string timestamp;
        bool isnumber;
    }




    address[] users_addresses_request;
    address[] users_addresses_accounts;


    mapping( address => request_struc ) req_map;
    mapping( address => accounts_struc) acc_map;



    function get_owner() public view returns(address){
        return owner;
    }

    function set_owner(address adr) public returns(string memory){
        owner = adr;
        return ("Ready");
    }

    function reg_forward(address adr, string memory number, string memory timestamp) public payable{

        users_addresses_accounts.push(adr);
        acc_map[adr] = accounts_struc(number, timestamp, true);

    }


    function unreg_forward(address adr) public payable{


        uint len = users_addresses_accounts.length;
        for(uint i=0; i<len;i++){

            if(users_addresses_accounts[i] == adr){

            acc_map[users_addresses_accounts[i]].number="";
            acc_map[users_addresses_accounts[i]].timestamp="";
            acc_map[users_addresses_accounts[i]].isnumber=false;

            users_addresses_accounts[i] = users_addresses_accounts[users_addresses_accounts.length-1];
            users_addresses_accounts.length = users_addresses_accounts.length-1;



        }
        }

    }


    function reg_request(string memory number, string memory timestamp) public payable{

        users_addresses_request.push(msg.sender);
        req_map[msg.sender] = request_struc(number, timestamp, true);
    }

    function unreg_request(string memory number, string memory timestamp) public payable{


        users_addresses_request.push(msg.sender);
        req_map[msg.sender] = request_struc(number, timestamp, false);
    }

    function request_cancel(address adr) public payable{
        uint len = users_addresses_request.length;
        for(uint i=0; i<len;i++){

            if(users_addresses_request[i] == adr){

            users_addresses_request[i] = users_addresses_request[users_addresses_request.length-1];
            users_addresses_request.length = users_addresses_request.length-1;
        }


    }
    }

    function reg_request_check(address adr)public view returns(string memory){
        uint len = users_addresses_request.length;
        bool trig = false;

        for (uint i=0; i<len; i++){
            if(users_addresses_request[i] == adr){
                trig = true;
            }
        }

        if(trig==false){
        return "Empty";

        }else{
            return "Full";
        }


    }


    function reg_account_check(address adr)public view returns(string memory){
        uint len = users_addresses_accounts.length;
        bool trig = false;

        for (uint i=0; i<len; i++){
            if(users_addresses_accounts[i] == adr){
                trig = true;
            }
        }

        if(trig==false){
        return "Empty";

        }else{
            return "Full";
        }


    }



    function get_address_from_phone(string memory number) public view returns(address){
        bool isHave = false;
        for (uint i=0; i<users_addresses_accounts.length; i++){

            if((keccak256(abi.encode(acc_map[users_addresses_accounts[i]].number)) == keccak256(abi.encode(number)))&&(acc_map[users_addresses_accounts[i]].isnumber==true)){
                isHave=true;
                return users_addresses_accounts[i];
            }
        }

        if(isHave==false){
            return 0x0000000000000000000000000000000000000000;
        }


    }

    function get_phone_from_address(address adr) public view returns(string memory){
        return acc_map[adr].number;
    }

    function get_timestamp_from_address(address adr) public view returns(string memory){

        return acc_map[adr].timestamp;
    }


    function get_status(address adr) public view returns(bool){
        return req_map[adr].isAdd;
    }

    function get_number_from_request(address adr)public view returns(string memory){
        return req_map[adr].number;
    }


}



