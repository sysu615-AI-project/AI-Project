#include <iostream>
#include "solution.hpp"
using namespace std;

int main() {
  int initial[9], target[9];
  cout << "Please enter the initial state:\n";
  for (int i = 0; i < 9; ++i) {
    cin >> initial[i];
  }
  cout << "Please enter the target state:\n";
  for (int i = 0; i < 9; ++i) {
    cin >> target[i];
  }
  Status node1(initial, NULL);
  Status node2(target, NULL);
  Solution solve(node1, node2);
  list<Status *> path = solve.AStarSolution();
  cout << path.size() << '\n';
  for (auto& c:path) {
    cout << *c << "->\n";
  }
  return 0;
}