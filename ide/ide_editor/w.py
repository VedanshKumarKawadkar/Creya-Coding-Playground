import requests
def func():
    api = "https://www.codechef.com/api/ide/submit"

    source_code = """
    #include <iostream>
    using namespace std;

    bool isPrime(int n)
    {
        if (n <= 1)
            return false;
        if (n <= 3)
            return true;
        if (n % 2 == 0 || n % 3 == 0)
            return false;
    
        for (int i = 5; i * i <= n; i = i + 6)
            if (n % i == 0 || n % (i + 2) == 0)
                return false;
    
        return true;
    }

    string solve(){
        string s;
        cin>>s;
        int x = stoi(s, 0, 2);
        if(isPrime(x)){
            return "Yes";
        }
        
        int n = s.length();
        for(int i=0; i<n-1; i++){
            if(s[i]=='1' && s[i+1]=='1'){
                return "Yes";
            }
            else if(s[i]=='1' && s[i+1]=='0'){
                return "Yes";
            }
        }
        return "No";
    }


    int main() {
        int n = 0;
        cin>>n;
        while(n--){
            cout<<solve()<<endl;
        }
        return 0;
    }
    """
    lang = "44"
    contest_code = "JAN221B"
    problem_code = "PINBS"

    data = {
        'source_code':source_code,
        'language':lang,
        'contestCode':contest_code,
        'problemCode':problem_code 
    }

    api_respose = requests.post(api, data).json()
    print(api_respose)
    

func()