#include "calculator.h"
#include "ui_calculator.h"

using namespace std;

const double eps = 1e-6;

Calculator::Calculator(QWidget *parent)
        : QMainWindow(parent), ui(new Ui::Calculator) {
    ui->setupUi(this);
    this->tmp = "";
}

Calculator::~Calculator() {
    delete ui;
}


void Calculator::on_num0_clicked() {
    if (this->tmp != "") {
        this->tmp += this->ui->num0->text();
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_num1_clicked() {
    this->tmp += this->ui->num1->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num2_clicked() {
    this->tmp += this->ui->num2->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num3_clicked() {
    this->tmp += this->ui->num3->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num4_clicked() {
    this->tmp += this->ui->num4->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num5_clicked() {
    this->tmp += this->ui->num5->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num6_clicked() {
    this->tmp += this->ui->num6->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num7_clicked() {
    this->tmp += this->ui->num7->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num8_clicked() {
    this->tmp += this->ui->num8->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_num9_clicked() {
    this->tmp += this->ui->num9->text();
    this->ui->resultbox->setText(this->tmp);
}

void Calculator::on_op_add_clicked() {
    if (tmp.endsWith("-") || tmp.endsWith("*") || tmp.endsWith("/")) {
        this->tmp = this->tmp.replace(tmp.length() - 1, 1, "+");
        this->ui->resultbox->setText(this->tmp);
    } else if (tmp != "" && !tmp.endsWith("+")) {
        this->tmp += this->ui->op_add->text();
        this->ui->resultbox->setText(this->tmp);
    }

}

void Calculator::on_op_sub_clicked() {
    if (tmp.endsWith("+") || tmp.endsWith("*") || tmp.endsWith("/")) {
        this->tmp = this->tmp.replace(tmp.length() - 1, 1, "-");
        this->ui->resultbox->setText(this->tmp);
    } else if (tmp != "" && !tmp.endsWith("-")) {
        this->tmp += this->ui->op_sub->text();
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_op_times_clicked() {
    if (tmp.endsWith("+") || tmp.endsWith("-") || tmp.endsWith("/")) {
        this->tmp = this->tmp.replace(tmp.length() - 1, 1, "*");
        this->ui->resultbox->setText(this->tmp);
    } else if (tmp != "" && !tmp.endsWith("*")) {
        this->tmp += this->ui->op_times->text();
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_op_div_clicked() {
    if (tmp.endsWith("+") || tmp.endsWith("-") || tmp.endsWith("*")) {
        this->tmp = this->tmp.replace(tmp.length() - 1, 1, "/");
        this->ui->resultbox->setText(this->tmp);
    } else if (tmp != "" && !tmp.endsWith("/")) {
        this->tmp += this->ui->op_div->text();
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_op_equal_clicked() {
    if (tmp != "") {
        Calculator::processCalculation(tmp);
        this->ui->resultbox->setText(this->tmp);
        this->tmp = "";
    }
}

void Calculator::on_op_dot_clicked() {
    if (tmp != " " && tmp != "" && !tmp.endsWith(".")) {
        this->tmp += this->ui->op_dot->text();
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_op_left_clicked() {
    if (tmp != " ") {
        this->tmp += this->ui->op_left->text();
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_op_right_clicked() {
    if (tmp != " ") {
        this->tmp += this->ui->op_right->text();
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_op_del_clicked() {
    if (tmp != " ") {
        tmp = tmp.left(tmp.length() - 1);
        this->ui->resultbox->setText(this->tmp);
    }
}

void Calculator::on_op_C_clicked() {
    tmp.clear();
    this->ui->resultbox->setText(0);
    this->tmp = "";
}

int Calculator::priority(int state, char a) {//计算操作符优先级的函数，注意state表示运算符状态：
//这个state只对‘（’起作用
    int result = 0;
    switch (a) {
        case '+':
        case '-':
            result = 1;
            break;
        case '*':
        case '/':
            result = 2;
            break;
        case '(':
            if (state == 0)
                result = 3;//（括号在栈里，等级高
            else
                result = 0;
            break;
        case '#':
            result = 0; //类似头结点和基准的作用
            break;
        default:
            break;
    }
    return result;
}

/* 直接执行计算的函数。
 *
 * @param op 运算符
 * @param op1 左操作数
 * @param op2 右操作数
 * @return 计算结果
 * @throws 除数为 0 时报错。
 * */
double Calculator::calculate(char op, double op1, double op2) {
    double result = 0;
    switch (op) {
        case '+':
            result = op1 + op2;
            break;
        case '-':
            result = op1 - op2;
            break;
        case '*':
            result = op1 * op2;
            break;
        case '/':
            // 处理除数为 0 的情况。
            if (op2 - 0 < eps) {
                throw std::runtime_error("错误：除数不能为 0");
            }
            result = op1 / op2;
            break;
        default:
            break;
    }
    return result;
}

/* 将输入的中缀表达式转换为后缀表达式并计算。
 *
 * @param tmp 输入的中缀表达式
 * @throws 括号不匹配时报错。
 * */
void Calculator::processCalculation(QString &tmp) {
    string s;
    s = tmp.toStdString();

    // 括号匹配检查。
    int bracketCount = 0;
    for (char c: s) {
        if (c == '(') bracketCount++;
        if (c == ')') bracketCount--;
        if (bracketCount < 0) {
            this->tmp = "错误：括号不匹配";
            this->ui->resultbox->setText(this->tmp);
            return;
        }
    }
    if (bracketCount != 0) {
        this->tmp = "错误：括号不匹配";
        this->ui->resultbox->setText(this->tmp);
        return;
    }

    // 连续操作符检查。
    for (int i = 1; i < s.length(); i++) {
        if ((s[i] == '+' || s[i] == '-' || s[i] == '*' || s[i] == '/') &&
            (s[i - 1] == '+' || s[i - 1] == '-' || s[i - 1] == '*' || s[i - 1] == '/')) {
            this->tmp = "错误：连续的操作符";
            this->ui->resultbox->setText(this->tmp);
            return;
        }
    }

    stack<char> operation;  // 存放操作符的栈。
    stack<double> operand;  // 存放操作数的栈。
    operation.push('#');  // 先将‘#’压栈。
    string num;  // 临时存放一个操作数，确保多位数和有小数点的数为一体。
    for (int i = 0; i < int(s.length()); i++) {
        if (isdigit(s[i])) {  // 出现数字。
            bool hasDecimalPoint = false;
            while (isdigit(s[i]) || s[i] == '.') {  // 将操作数提取完全。
                if (s[i] == '.') {
                    // 处理多余小数点。
                    if (hasDecimalPoint) {
                        this->tmp = "错误：多个小数点";
                        this->ui->resultbox->setText(this->tmp);
                        return;
                    }
                    hasDecimalPoint = true;
                }
                num.push_back(s[i]);
                i++;
            }
            double a = atof(num.c_str());  // string->double
            cout << "in num: " << a << endl; // console 中显示，方便调试。
            operand.push(a);  // 操作数入栈。
            num.clear();  // num临时变量清空以备下次使用。
            i--;  // 位置还原。
        } else if (s[i] == '+' || s[i] == '-'
                   || s[i] == '*' || s[i] == '/'
                   || s[i] == '(') { // 出现运算符。
            if (priority(0, s[i])
                > priority(1, operation.top()))
                // 优先级比较，计算操作符优先级的函数，
                // 注意 state 表示运算符状态：state = 1 表示还未进栈，
                // state = 0 表示栈内优先级，注意。
            {
                cout << "in op: " << s[i] << endl;
                operation.push(s[i]);
            }
                // 当当前的符号放在栈内，比前一个符号等级高时，直接入栈，比如+比#等级高，*比+等级高，（比*等级高
            else {
                while (priority(0, s[i])
                       <= priority(1, operation.top())) {
                    // 当当前的符号放在栈内，比前一个符号等级（对于（括号是在栈外的等级）低时，出栈并进行计算直至>
                    char temp = operation.top();
                    cout << "out op: " << temp << endl;
                    operation.pop();
                    double op2 = operand.top();
                    cout << "out op2: " << op2 << endl;
                    operand.pop();
                    double op1 = operand.top();
                    cout << "out op1: " << op1 << endl;
                    operand.pop();
                    operand.push(calculate(temp, op1, op2));
                    cout << "in result: " << operand.top() << endl;
                }
                operation.push(s[i]); // 不要忘了最后操作符入栈！！！！！特别是在左括号时特别重要
                cout << "in op: " << s[i] << endl;
            }
        } else if (s[i] == ')') { // 扫描到‘)’
            while (operation.top() != '(') { // 出栈直至‘(’
                char temp = operation.top();
                cout << "out op: " << temp << endl;
                operation.pop();
                double op2 = operand.top();
                cout << "out op2: " << op2 << endl;
                operand.pop();
                double op1 = operand.top();
                cout << "out op1: " << op1 << endl;
                operand.pop();
                operand.push(calculate(temp, op1, op2));
                cout << "in result: " << operand.top() << endl;
            }
            operation.pop();// ‘(’出栈
            cout << "out op: " << s[i] << endl;
        } else { // 非法字符的处理比如字母
            this->tmp = "error!";
            this->ui->resultbox->setText(this->tmp);
            break;
        }
    }
    while (operation.top() != '#') { // 扫尾工作
        char temp = operation.top();
        cout << "out op: " << temp << endl;
        operation.pop();
        double op2 = operand.top();
        cout << "out op2: " << op2 << endl;
        operand.pop();
        double op1 = operand.top();
        cout << "out op1: " << op1 << endl;
        operand.pop();
        operand.push(calculate(temp, op1, op2));
        cout << "in result: " << operand.top() << endl;
    }
    this->tmp = QString("= ");
    this->tmp += tmp.number(operand.top());
    this->ui->resultbox->setText(this->tmp);
}
