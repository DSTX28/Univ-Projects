module fuel_needed_calculator (
    input  signed [15:0] distance,
    input  signed [15:0] efficiency,
    output signed [15:0] fuel_needed
);
    assign fuel_needed = distance / efficiency;
endmodule
