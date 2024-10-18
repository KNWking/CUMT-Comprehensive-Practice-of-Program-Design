#include "calculator.h"
#include "ui_calculator.h"

using namespace std;

const double eps = 1e-6;

Calculator::Calculator(QWidget *parent)
        : QMainWindow(parent), ui(new Ui::Calculator) {
    ui->setupUi(this);
    this->rowFormula = "";
}

Calculator::~Calculator() {
    delete ui;
}


void Calculator::on_num0_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    if (this->rowFormula != "0" || (*(rowFormula.begin()) != '=')) {
        this->rowFormula += this->ui->num0->text();
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_num1_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num1->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num2_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num2->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num3_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num3->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num4_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num4->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num5_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num5->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num6_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num6->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num7_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num7->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num8_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num8->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_num9_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    this->rowFormula += this->ui->num9->text();
    this->ui->resultbox->setText(this->rowFormula);
}

void Calculator::on_op_add_clicked() {
    if (*(rowFormula.begin()) == 'e') {
        rowFormula = "";
    }
    if (rowFormula.endsWith("-") || rowFormula.endsWith("*") || rowFormula.endsWith("/")) {
        this->rowFormula = this->rowFormula.replace(rowFormula.length() - 1, 1, "+");
        this->ui->resultbox->setText(this->rowFormula);
        return;
    }
    if (*(rowFormula.begin()) == '=') {
        rowFormula = this->rowFormula.mid(2);
    }
    if (rowFormula != "" && !rowFormula.endsWith("+")) {
        this->rowFormula += this->ui->op_add->text();
        this->ui->resultbox->setText(this->rowFormula);
    }

}

void Calculator::on_op_sub_clicked() {
    if (*(rowFormula.begin()) == 'e') {
        rowFormula = "";
    }
    if (rowFormula.endsWith("+") || rowFormula.endsWith("*") || rowFormula.endsWith("/")) {
        this->rowFormula = this->rowFormula.replace(rowFormula.length() - 1, 1, "-");
        this->ui->resultbox->setText(this->rowFormula);
        return;
    }
    if (*(rowFormula.begin()) == '=') {
        rowFormula = this->rowFormula.mid(2);
    }
    if (rowFormula != "" && !rowFormula.endsWith("-")) {
        this->rowFormula += this->ui->op_sub->text();
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_times_clicked() {
    if (*(rowFormula.begin()) == 'e') {
        rowFormula = "";
    }
    if (rowFormula.endsWith("+") || rowFormula.endsWith("-") || rowFormula.endsWith("/")) {
        this->rowFormula = this->rowFormula.replace(rowFormula.length() - 1, 1, "*");
        this->ui->resultbox->setText(this->rowFormula);
        return;
    }
    if (*(rowFormula.begin()) == '=') {
        rowFormula = this->rowFormula.mid(2);
    }
    if (rowFormula != "" && !rowFormula.endsWith("*")) {
        this->rowFormula += '*';
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_div_clicked() {
    if (*(rowFormula.begin()) == 'e') {
        rowFormula = "";
    }
    if (rowFormula.endsWith("+") || rowFormula.endsWith("-") || rowFormula.endsWith("*")) {
        this->rowFormula = this->rowFormula.replace(rowFormula.length() - 1, 1, "/");
        this->ui->resultbox->setText(this->rowFormula);
        return;
    }
    if (*(rowFormula.begin()) == '=') {
        rowFormula = this->rowFormula.mid(2);
    }
    if (rowFormula != "" && !rowFormula.endsWith("/")) {
        this->rowFormula += '/';
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_equal_clicked() {
    if (rowFormula != "" && (*(rowFormula.begin()) != '=') && (*(rowFormula.begin()) != 'e')) {
        Calculator::processCalculation(rowFormula);
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_dot_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    if (rowFormula != " " && rowFormula != ""
        && !rowFormula.endsWith(".")
        && !rowFormula.toStdString().find('.')) {
        this->rowFormula += this->ui->op_dot->text();
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_left_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    if (rowFormula != " " || *rowFormula.begin() != '=') {
        this->rowFormula += this->ui->op_left->text();
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_right_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    if (rowFormula != " " || *rowFormula.begin() != '=') {
        this->rowFormula += this->ui->op_right->text();
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_del_clicked() {
    if ((*(rowFormula.begin()) == '=') || (*(rowFormula.begin()) == 'e')) {
        rowFormula = "";
    }
    if (rowFormula != " " || *rowFormula.begin() != '=') {
        rowFormula = rowFormula.left(rowFormula.length() - 1);
        this->ui->resultbox->setText(this->rowFormula);
    }
}

void Calculator::on_op_C_clicked() {
    rowFormula.clear();
    this->ui->resultbox->setText(0);
    this->rowFormula = "";
}

// 计算操作符优先级的函数，state 表示运算符状态：
int Calculator::priority(int state, char a) {
    // 这个 state 只对‘(’起作用
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
            // 返回无穷大表示错误。
            if (abs(op2 - 0) < eps) {
                return numeric_limits<double>::infinity();
            }
            result = op1 / op2;
            break;
        default:
            break;
    }
    return result;
}

// 括号匹配检查。
bool Calculator::ifBracketsBalanced(const string &str) {
    int leftBracketCount = 0;
    for (char ch: str) {
        if (ch == '(') {
            leftBracketCount++;
        } else if (ch == ')') {
            if (leftBracketCount == 0) {
                return false;
            } else {
                leftBracketCount--;
            }
        }
    }
    // 0 说明左右括号数量一致。
    return leftBracketCount == 0;
}


/* 将输入的中缀表达式转换为后缀表达式并计算。
 *
 * @param rowFormula 输入的中缀表达式
 * @throws 括号不匹配时报错。
 * */
void Calculator::processCalculation(QString &rowFormula) {
    string s;
    s = rowFormula.toStdString();

    if (!ifBracketsBalanced(s)) {
        this->rowFormula = "error：括号不匹配";
        this->ui->resultbox->setText(this->rowFormula);
        return;
    }

    // 连续操作符检查。
    for (int i = 1; i < s.length(); i++) {
        if ((s[i] == '+' || s[i] == '-' || s[i] == '*' || s[i] == '/') &&
            (s[i - 1] == '+' || s[i - 1] == '-' || s[i - 1] == '*' || s[i - 1] == '/')) {
            this->rowFormula = "error：连续的操作符";
            this->ui->resultbox->setText(this->rowFormula);
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
                        this->rowFormula = "error：多个小数点";
                        this->ui->resultbox->setText(this->rowFormula);
                        return;
                    }
                    hasDecimalPoint = true;
                }
                num.push_back(s[i]);
                i++;
            }
            double a = atof(num.c_str());  // string->double
            operand.push(a);  // 操作数入栈。
            num.clear();  // num临时变量清空以备下次使用。
            i--;  // 位置还原。
        } else if (s[i] == '+' || s[i] == '-'
                   || s[i] == '*' || s[i] == '/'
                   || s[i] == '(') { // 出现运算符。
            // 优先级比较，计算操作符优先级的函数，
            // 注意 state 表示运算符状态：state = 1 表示还未进栈，
            // state = 0 表示栈内优先级，注意。
            if (priority(0, s[i])
                > priority(1, operation.top())) {
                operation.push(s[i]);
            }
                // 当当前的符号放在栈内，比前一个符号等级高时，直接入栈，比如+比#等级高，*比+等级高，（比*等级高
            else {
                while (priority(0, s[i])
                       <= priority(1, operation.top())) {
                    // 当当前的符号放在栈内，比前一个符号等级（对于（括号是在栈外的等级）低时，出栈并进行计算直至>
                    char temp = operation.top();
                    operation.pop();
                    double op2 = operand.top();
                    operand.pop();
                    double op1 = operand.top();
                    operand.pop();
                    double result = calculate(temp, op1, op2);
                    if (std::isinf(result)) {
                        this->rowFormula = "error：除数不能为零";
                        this->ui->resultbox->setText(this->rowFormula);
                        return;
                    }
                    operand.push(result);
                }
                operation.push(s[i]); // 不要忘了最后操作符入栈！！！！！特别是在左括号时特别重要
            }
        } else if (s[i] == ')') { // 扫描到‘)’
            while (operation.top() != '(') { // 出栈直至‘(’
                char temp = operation.top();
                operation.pop();
                double op2 = operand.top();
                operand.pop();
                double op1 = operand.top();
                operand.pop();
                double result = calculate(temp, op1, op2);
                if (std::isinf(result)) {
                    this->rowFormula = "error：除数不能为零";
                    this->ui->resultbox->setText(this->rowFormula);
                    return;
                }
                operand.push(result);
            }
            operation.pop();// ‘(’出栈
        } else { // 非法字符的处理比如字母
            this->rowFormula = "error!";
            this->ui->resultbox->setText(this->rowFormula);
            break;
        }
    }
    while (operation.top() != '#') { // 扫尾工作
        char temp = operation.top();
        operation.pop();
        double op2 = operand.top();
        operand.pop();
        double op1 = operand.top();
        operand.pop();
        double result = calculate(temp, op1, op2);
        if (std::isinf(result)) {
            this->rowFormula = "error：除数不能为零";
            this->ui->resultbox->setText(this->rowFormula);
            return;
        }
        operand.push(result);
    }
    this->rowFormula = QString("= ");
    this->rowFormula += rowFormula.number(operand.top());
    this->ui->resultbox->setText(this->rowFormula);
}
