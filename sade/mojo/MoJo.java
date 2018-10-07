
public class MoJo {

	
    public static void main (String[] args){
        try
        {
            String sourceFile = null, targetFile = null, relFile = null;
            MoJoCalculator mjc;
            if (args.length < 2 || args.length > 4)
            {
			System.out.println("Error");
            }
            sourceFile = args[0];
            targetFile = args[1];
            if (args.length > 2)
            {
                /* -m+ indicates single direction MoJoPlus */
                if (args[2].equalsIgnoreCase("-m+"))
                {
                    mjc = new MoJoCalculator(sourceFile, targetFile, relFile);
                    System.out.println(mjc.mojoplus());
                }
                else
                /* -b+ indicates double direction MoJoPlus */
                if (args[2].equalsIgnoreCase("-b+"))
                {
                    mjc = new MoJoCalculator(sourceFile, targetFile, relFile);
                    long one = mjc.mojoplus();
                    mjc = new MoJoCalculator(targetFile, sourceFile, relFile);
                    long two = mjc.mojoplus();
                    System.out.println(Math.min(one, two));
                }
                else
                /* -b indicates double direction MoJo */
                if (args[2].equalsIgnoreCase("-b"))
                {
                    mjc = new MoJoCalculator(sourceFile, targetFile, relFile);
                    long one = mjc.mojo();
                    mjc = new MoJoCalculator(targetFile, sourceFile, relFile);
                    long two = mjc.mojo();
                    System.out.println(Math.min(one, two));
                }
                else
                /* -fm asks for MoJoFM value */
                if (args[2].equalsIgnoreCase("-fm"))
                {
                    mjc = new MoJoCalculator(sourceFile, targetFile, relFile);
                   
                    System.out.println(mjc.mojofm());
                }
                else
                // -e indicates EdgeMoJo (requires extra argument)
                if (args[2].equalsIgnoreCase("-e"))
                {
                    if (args.length == 4)
                    {
                        relFile = args[3];
                        mjc = new MoJoCalculator(sourceFile, targetFile, relFile);
                        System.out.println(mjc.edgemojo());
                    }
                    else
                    {
			System.out.println("Error");
                    }
                }
                else
                {
			System.out.println("Error");
                }

            }
            else
            {
                mjc = new MoJoCalculator(sourceFile, targetFile, relFile);
                System.out.println(mjc.mojo());
            }
        }
        catch (RuntimeException e)
        {
            System.out.println(e.getMessage());
            
        }
        
    }

  
}
