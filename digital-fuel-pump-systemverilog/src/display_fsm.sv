module display_fsm (
    input  logic        clk,
    input  logic        reset,
    input  logic [15:0] total_cost,
    output reg   [6:0]  segment_1,
    output reg   [6:0]  segment_2,
    output reg   [6:0]  segment_3,
    output reg   [6:0]  segment_4
);
    reg [3:0] digit_1, digit_2, digit_3, digit_4;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            digit_1 <= 0;
            digit_2 <= 0;
            digit_3 <= 0;
            digit_4 <= 0;
        end else begin
            digit_1 <= total_cost % 10;
            digit_2 <= (total_cost / 10) % 10;
            digit_3 <= (total_cost / 100) % 10;
            digit_4 <= (total_cost / 1000) % 10;
        end
    end

    seven_segment_display display1 (.digit(digit_1), .segments(segment_1));
    seven_segment_display display2 (.digit(digit_2), .segments(segment_2));
    seven_segment_display display3 (.digit(digit_3), .segments(segment_3));
    seven_segment_display display4 (.digit(digit_4), .segments(segment_4));

endmodule
