class Main inherits IO {
    a : Int <- 1;
    main() : Object { 
        {
            out_string("Hello, world.\n");
            out_int(a);
        }
    };
}; 