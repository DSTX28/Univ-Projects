module testbench;

    reg signed [15:0] distance;
    reg signed [15:0] efficiency;
    reg signed [15:0] cost_per_liter;
    reg clk;
    reg reset;

    wire [6:0] segment_1, segment_2, segment_3, segment_4;

    top_level uut (
        .distance(distance),
        .efficiency(efficiency),
        .cost_per_liter(cost_per_liter),
        .clk(clk),
        .reset(reset),
        .segment_1(segment_1),
        .segment_2(segment_2),
        .segment_3(segment_3),
        .segment_4(segment_4)
    );

    always begin
        #5 clk = ~clk;
    end

    initial begin
        clk = 0;
        reset = 1;
        distance = 100;
        efficiency = 10;
        cost_per_liter = 5;

        #10 reset = 0;
        #50;

        distance = 200;
        efficiency = 5;
        cost_per_liter = 4;

        #50;
        $finish;
    end

endmodule
