#ifndef MORTGAGECALCULATOR_H
#define MORTGAGECALCULATOR_H

#include <QMainWindow>
#include <QRadioButton>
#include <cmath>
#include <cstring>

class MortgageCalculator {
public:
    enum RepaymentType {
        EqualPayment, EqualPrincipal
    };

    MortgageCalculator();

    void setLoanTerm(int years);

    void setLoanAmount(double amount);

    void setInterestRate(double rate);

    void setRepaymentType(RepaymentType type);

    double calculateMonthlyPayment();

    double calculateTotalInterest();

    double calculateTotalPayment();

private:
    int loanTerm;
    double loanAmount;
    double interestRate;
    RepaymentType repaymentType;
};

#endif // MORTGAGECALCULATOR_H
