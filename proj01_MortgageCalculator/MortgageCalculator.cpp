#include "MortgageCalculator.h"

MortgageCalculator::MortgageCalculator()
        : loanTerm(0), loanAmount(0.0), interestRate(0.0), repaymentType(EqualPayment) {
}

void MortgageCalculator::setLoanTerm(int years) {
    loanTerm = years;
}

void MortgageCalculator::setLoanAmount(double amount) {
    loanAmount = amount;
}

void MortgageCalculator::setInterestRate(double rate) {
    interestRate = rate;
}

void MortgageCalculator::setRepaymentType(RepaymentType type) {
    repaymentType = type;
}

double MortgageCalculator::calculateMonthlyPayment() {
    double monthlyRate = interestRate / 12 / 100;
    int totalMonths = loanTerm * 12;

    if (repaymentType == EqualPayment) {
        return loanAmount * monthlyRate * std::pow(1 + monthlyRate, totalMonths)
               / (std::pow(1 + monthlyRate, totalMonths) - 1);
    } else {
        // Equal Principal calculation
        double principal = loanAmount / totalMonths;
        return principal + loanAmount * monthlyRate;
    }
}

double MortgageCalculator::calculateTotalInterest() {
    return calculateTotalPayment() - loanAmount;
}

double MortgageCalculator::calculateTotalPayment() {
    if (repaymentType == EqualPayment) {
        return calculateMonthlyPayment() * loanTerm * 12;
    } else {
        // For Equal Principal, we need to sum up all payments
        double totalPayment = 0;
        double monthlyRate = interestRate / 12 / 100;
        int totalMonths = loanTerm * 12;
        double monthlyPrincipal = loanAmount / totalMonths;

        for (int i = 0; i < totalMonths; ++i) {
            double remainingBalance = loanAmount - (monthlyPrincipal * i);
            totalPayment += monthlyPrincipal + (remainingBalance * monthlyRate);
        }
        return totalPayment;
    }
}
