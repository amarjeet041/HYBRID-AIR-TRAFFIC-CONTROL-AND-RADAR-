#include <bits/stdc++.h>
using namespace std;

//////////////////////////////////////////////////////
// ✈️ FLIGHT PRIORITY SYSTEM
//////////////////////////////////////////////////////

void flightPriority() {
    string flightID;
    int fuel, emergency;

    cin >> flightID >> fuel >> emergency;

    time_t now = time(0);

    cout << "\n===== ATC CONTROL =====\n";
    cout << "Time: " << ctime(&now);
    cout << "Flight: " << flightID << endl;
    cout << "Fuel Level: " << fuel << endl;

    if (emergency == 1) {
        cout << "Status: EMERGENCY LANDING 🚨\n";
    }
    else if (fuel < 20) {
        cout << "Status: CRITICAL FUEL ⚠️\n";
    }
    else if (fuel < 40) {
        cout << "Status: PRIORITY LANDING\n";
    }
    else {
        cout << "Status: NORMAL LANDING\n";
    }

    int runway = (emergency == 1) ? 1 : rand() % 3 + 1;
    cout << "Assigned Runway: " << runway << endl;

    cout << "-----------------------------\n";
}

//////////////////////////////////////////////////////
// 🚨 DUPLICATE FLIGHT CHECK
//////////////////////////////////////////////////////

void duplicateFlight() {
    vector<int> flights = {101, 202, 303, 101};

    unordered_set<int> s;
    for (int f : flights) {
        if (s.count(f)) {
            cout << "Duplicate Flight ID Detected: " << f << endl;
            return;
        }
        s.insert(f);
    }
}

//////////////////////////////////////////////////////
// ✈️ AIRCRAFT OPERATIONS
//////////////////////////////////////////////////////

void aircraftOps() {
    cout << "Passenger Aircraft Landing...\n";
    cout << "Cargo Aircraft Handling Logistics...\n";
}

//////////////////////////////////////////////////////
// 📡 SIGNAL SYSTEM
//////////////////////////////////////////////////////

void signalSystem() {
    cout << "Normal Signal Active\n";
    cout << "Emergency Signal Detected 🚨\n";
}

//////////////////////////////////////////////////////
// 🧠 RADAR MEMORY (LRU SIMULATION)
//////////////////////////////////////////////////////

void radarMemory() {
    vector<int> memory = {101, 202, 303, 101, 404};

    cout << "Radar Memory Tracking: ";
    for (int m : memory)
        cout << m << " ";
    cout << endl;
}

//////////////////////////////////////////////////////
// 🌍 AIR ROUTE NAVIGATION (BFS)
//////////////////////////////////////////////////////

void airRoute() {
    int V = 5;
    vector<vector<int>> adj(V, vector<int>(V, 0));

    adj[0][1] = adj[1][0] = 1;
    adj[1][2] = adj[2][1] = 1;
    adj[2][3] = adj[3][2] = 1;
    adj[3][4] = adj[4][3] = 1;

    vector<bool> vis(V, false);
    queue<int> q;

    q.push(0);
    vis[0] = true;

    cout << "Air Route Path: ";

    while (!q.empty()) {
        int node = q.front(); q.pop();
        cout << node << " ";

        for (int i = 0; i < V; i++) {
            if (adj[node][i] && !vis[i]) {
                vis[i] = true;
                q.push(i);
            }
        }
    }

    cout << endl;
}

//////////////////////////////////////////////////////
// 🚀 MAIN FUNCTION
//////////////////////////////////////////////////////

int main() {
    int choice;
    cin >> choice;

    if (choice == 1) {
        flightPriority();
    }
    else if (choice == 2) {
        duplicateFlight();
    }
    else if (choice == 3) {
        aircraftOps();
    }
    else if (choice == 4) {
        signalSystem();
    }
    else if (choice == 5) {
        radarMemory();
    }
    else if (choice == 6) {
        airRoute();
    }

    return 0;
}
