#ifndef MORTGAGECALCULATOR_H
#define MORTGAGECALCULATOR_H

#include <QMainWindow>
#include <QMessageBox>
#include <cmath>
#include <cstring>

QT_BEGIN_NAMESPACE
namespace Ui {
    class MortgageCalculator;
}
QT_END_NAMESPACE

class MortgageCalculator : public QMainWindow {
Q_OBJECT

public:
    MortgageCalculator(QWidget *parent = nullptr);

    ~MortgageCalculator();

private slots:

    void on_calculate_clicked();

    void on_reset_clicked();

private:
    Ui::MortgageCalculator *ui;

    double loanTerm;
    double loanAmount;
    double interestRate;

    int repaymentType;

    double monthlyPayment;
    double totalInterest;
    double totalPayment;

    void setLoanTerm(double years);

    void setLoanAmount(double amount);

    void setInterestRate(double rate);

    void setRepaymentType(int type);

    void calculateEqualPayment();

    void calculateEqualPrincipal();

    void displayResults(double monthlyPayment, double totalInterest, double totalPayment);

    void resetFields();

    bool validateInputs() const;
};

#endif // MORTGAGECALCULATOR_H
