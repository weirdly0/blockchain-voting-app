// import "../css/style.css"

const Web3 = require('web3');
const contract = require('@truffle/contract');

const votingArtifacts = require('../../build/contracts/Voting.json');
var VotingContract = contract(votingArtifacts);

window.App = {
  eventStart: async function() { 
    try {
        // Request access to Metamask accounts
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });

        if (accounts.length === 0) {
            console.error("No accounts found. Please connect your Metamask wallet.");
            return;
        }

        // Set the account and provider
        App.account = accounts[0]; 
        VotingContract.setProvider(window.ethereum);
        VotingContract.defaults({ from: App.account, gas: 6654755 });

        // Display account on UI
        $("#accountAddress").html("Your Account: " + App.account);

        // Load contract
        const instance = await VotingContract.deployed();

        // Fetch candidate count
        const countCandidates = await instance.getCountCandidates();

        $(document).ready(function() {
            $('#addCandidate').click(async function() {
                const nameCandidate = $('#name').val();
                const partyCandidate = $('#party').val();

                if (!nameCandidate || !partyCandidate) {
                    console.error("Please enter candidate details.");
                    return;
                }

                try {
                    await instance.addCandidate(nameCandidate, partyCandidate, { from: App.account });
                    console.log("Candidate added successfully.");
                } catch (error) {
                    console.error("ERROR! " + error.message);
                }
            });

            $('#addDate').click(async function() {
                const startDate = Date.parse(document.getElementById("startDate").value) / 1000;
                const endDate = Date.parse(document.getElementById("endDate").value) / 1000;

                try {
                    await instance.setDates(startDate, endDate, { from: App.account });
                    console.log("Dates set successfully.");
                } catch (error) {
                    console.error("ERROR! " + error.message);
                }
            });
        });

        // Display voting dates
        try {
            const result = await instance.getDates();
            const startDate = new Date(result[0] * 1000);
            const endDate = new Date(result[1] * 1000);
            $("#dates").text(startDate.toDateString() + " - " + endDate.toDateString());
        } catch (err) {
            console.error("ERROR! " + err.message);
        }

        // Display candidates
        for (let i = 0; i < countCandidates; i++) {
            try {
                const data = await instance.getCandidate(i + 1);
                const id = data[0];
                const name = data[1];
                const party = data[2];
                const voteCount = data[3];
                const viewCandidates = `<tr>
                    <td><input class="form-check-input" type="radio" name="candidate" value="${id}" id=${id}> ${name}</td>
                    <td>${party}</td>
                    <td>${voteCount}</td>
                </tr>`;
                $("#boxCandidate").append(viewCandidates);
            } catch (error) {
                console.error("ERROR retrieving candidate: " + error.message);
            }
        }

        // Check if user has already voted
        const voted = await instance.checkVote();
        if (!voted) {
            $("#voteButton").attr("disabled", false);
        }

    } catch (error) {
        console.error("ERROR! " + error.message);
    }
  },

  vote: async function() {    
    const candidateID = $("input[name='candidate']:checked").val();

    if (!candidateID) {
        $("#msg").html("<p>Please vote for a candidate.</p>");
        return;
    }

    try {
        const instance = await VotingContract.deployed();
        await instance.vote(parseInt(candidateID), { from: App.account });

        $("#voteButton").attr("disabled", true);
        $("#msg").html("<p>Voted successfully!</p>");

        setTimeout(() => {
            window.location.reload();
        }, 1000);
        
    } catch (err) {
        console.error("ERROR! " + err.message);
    }
  }
};

window.addEventListener("load", async function() {
  if (typeof window.ethereum !== "undefined") {
    console.warn("Using Web3 detected from external source like Metamask");
    window.web3 = new Web3(window.ethereum);
  } else {
    console.warn("No Web3 detected. Falling back to http://localhost:9545. You should remove this fallback when you deploy live, as it's inherently insecure. Consider switching to Metamask for deployment. More info here: http://truffleframework.com/tutorials/truffle-and-metamask");
    window.web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:9545"));
  }
  await window.App.eventStart();
});
