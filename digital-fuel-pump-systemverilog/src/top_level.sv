module top_level (
    input  signed [15:0] distance,
    input  signed [15:0] efficiency,
    input  signed [15:0] cost_per_liter,
    input  logic         clk,
    input  logic         reset,
    output [6:0]         segment_1,
    output [6:0]         segment_2,
    output [6:0]         segment_3,
    output [6:0]         segment_4
);
    wire signed [15:0] fuel_needed;
    wire signed [15:0] total_cost;

    fuel_needed_calculator fuel_calc (
        .distance(distance),
        .efficiency(efficiency),
        .fuel_needed(fuel_needed)
    );

    cost_calculator cost_calc (
        .fuel_needed(fuel_needed),
        .cost_per_liter(cost_per_liter),
        .total_cost(total_cost)
    );

    display_fsm display (
        .clk(clk),
        .reset(reset),
        .total_cost(total_cost),
        .segment_1(segment_1),
        .segment_2(segment_2),
        .segment_3(segment_3),
        .segment_4(segment_4)
    );

endmodule
