module cost_calculator (
    input  signed [15:0] fuel_needed,
    input  signed [15:0] cost_per_liter,
    output signed [15:0] total_cost
);
    assign total_cost = fuel_needed * cost_per_liter;
endmodule
