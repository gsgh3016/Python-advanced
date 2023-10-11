#include <iostream>
#include <string>

using namespace std;

int main()
{
    string stack_array[3] = {"abc", "def", "ghi"};

    cout << "stack_array start address: " << &stack_array << endl;

    for (string &str : stack_array)
    {
        cout << "string: " << str << " string address: " << &str << endl;
    }
    cout << endl;
    string *heap_array = new string[3];
    heap_array[0] = "hij";
    heap_array[1] = "klm";
    heap_array[2] = "nop";

    cout << "heap_array start address: " << heap_array << endl;
    // cout << &heap_array << endl;
    for (int i = 0; i < 3; i++)
    {
        cout << "string: " << heap_array[i] << " string address: " << &heap_array[i] << endl;
    }
    return 0;
}